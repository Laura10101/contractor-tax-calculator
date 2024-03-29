"""Define views for the forms API."""

from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django.core.exceptions import SuspiciousOperation
import json
from .serializers import *
from .services import *
from .models import BooleanQuestion, NumericQuestion, MultipleChoiceQuestion


class FormsList(APIView):
    """Create django rest forms list view."""
    """Django rest views are classes inheriting APIView"""

    def post(self, request):
        """Create a new form via the Forms API."""

        # Extract relevant data from http request
        # For a post request, we get the data from the body of the http request
        # Get jurisdiction id from http body
        # The request parameter is already a python dictionary
        if 'jurisdiction_id' not in request.data.keys():
            # Code to return an HTTP 400 error
            # https://stackoverflow.com/questions/23492000/how-to-return-http-400-response-in-django
            return Response(
                {
                    'error': 'Invalid request. Please specify jurisdiction ' +
                    'ID for the new form.'
                },
                status=status.HTTP_400_BAD_REQUEST
                )
        jurisdiction_id = request.data['jurisdiction_id']
        # Call apropriate services method
        try:
            form_id = create_form(jurisdiction_id)
        except ValidationError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
                )
        except IntegrityError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_409_CONFLICT
                )
        # Create response
        response = {
            'form_id': form_id
        }
        # Return response
        return Response(response)

    def get(self, request):
        """Get the forms based on a specified list of jurisdiction IDs"""

        # Extract relevant data from http request
        # Services method expects a list of jurisdiction ids
        # List of jurisdiction ids will be provded as comma separated
        # list in query string
        # Get value of ids parameter from http request (query string)
        if 'jurisdiction_ids' not in request.GET.keys():
            print('No jurisdiction_ids found in request')
            # Code to return an HTTP 400 error
            # https://stackoverflow.com/questions/23492000/how-to-return-http-400-response-in-django
            return Response(
                {
                    'error': 'Invalid request. Please specify jurisdiction IDs'
                },
                status=status.HTTP_400_BAD_REQUEST
                )
        id_string = request.GET['jurisdiction_ids']
        # Split string into array of strings
        id_strings = id_string.split(',')
        # Parse the array of string values into an array integers
        id_ints = list(map(int, id_strings))
        # Call apropriate services method
        # Create variable to contain results of get method
        forms = get_forms_by_jurisdiction_ids(id_ints)
        # Create response
        # Now to translate this into JSON data
        # Generate dictionary of form data listed by jurisdiciton id
        forms_by_jurisdiction_id = {}
        for form in forms:
            questions = []
            for question in form.questions.order_by('ordinal').all():
                serialised_question = {
                    'id': question.id,
                    'text': question.text,
                    'explainer': question.explainer,
                    'is_mandatory': question.is_mandatory,
                    'variable_name': question.variable_name,
                    'ordinal': question.ordinal,
                }

                if isinstance(question, BooleanQuestion):
                    serialised_question['type'] = 'boolean'
                elif isinstance(question, NumericQuestion):
                    serialised_question['type'] = 'numeric'
                    serialised_question['is_integer'] = question.is_integer
                    serialised_question['min_value'] = question.min_value
                    serialised_question['max_value'] = question.max_value
                elif isinstance(question, MultipleChoiceQuestion):
                    serialised_question['type'] = 'multiple_choice'
                    serialised_question['options'] = []
                    for option in question.options.all():
                        serialised_question['options'].append({
                            'id': option.id,
                            'text': option.text,
                            'explainer': option.explainer,
                        })

                questions.append(serialised_question)

            forms_by_jurisdiction_id[form.jurisdiction_id] = {
                'id': form.id,
                'jurisdiction_id': form.jurisdiction_id,
                'questions': questions,
            }
        print(forms_by_jurisdiction_id)
        # Package the JSON data up into a response object
        response = {
            'forms': forms_by_jurisdiction_id
        }
        # Sending the Json response back to the client
        return Response(response)


# Create django rest form question list view
class FormQuestionList(APIView):
    """Create django rest form question list view."""

    def post(self, request, form_pk):
        """Create a new question within the given form."""

        # Validate common required attributes
        common_attributes = [
            'text',
            'ordinal',
            'explainer',
            'variable_name',
            'is_mandatory',
            'type',
        ]
        for attribute in common_attributes:
            if attribute not in request.data.keys():
                return Response(
                    {
                        'error': 'Invalid request. Please supply ' + attribute
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Extract relevant informaiton from JSON object into set of variables
        text = request.data['text']
        ordinal = request.data['ordinal']
        explainer = request.data['explainer']
        variable_name = request.data['variable_name']
        is_mandatory = request.data['is_mandatory']

        # Call the apropriate post method depending on Q type, using switch
        # statement
        try:
            match request.data['type']:
                case "boolean":
                    question_id = create_boolean_question(
                        form_pk,
                        text,
                        ordinal,
                        explainer,
                        variable_name,
                        is_mandatory
                    )

                case "numeric":
                    question_id = self.__post_numeric_question(
                        request,
                        form_pk,
                        text,
                        ordinal,
                        explainer,
                        variable_name,
                        is_mandatory
                    )

                case "multiple_choice":
                    question_id = create_multiple_choice_question(
                        form_pk,
                        text,
                        ordinal,
                        explainer,
                        variable_name,
                        is_mandatory
                    )

                case _:
                    return Response(
                        {
                            'error': 'Invalid request. Type should be: '
                            + 'boolean, numeric or multiple_choice'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
        except ValidationError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except IntegrityError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Form.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        if question_id == 0:
            return Response(
                {
                    'error': 'Invalid request. Please supply all required'
                    + ' attributes'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({
            'id': question_id
        })

    # Private controller methods to handle creating questions
    # with specific attributes

    # Method to create Numeric question
    def __post_numeric_question(
        self,
        request,
        form_pk,
        text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    ):
        # Validate that the specific attributes required are present
        specific_attributes = [
            'is_integer',
            'min_value',
            'max_value',
        ]
        for attribute in specific_attributes:
            if attribute not in request.data.keys():
                return 0

        # Extract specific attributes from JSON data
        is_integer = request.data['is_integer']
        min_value = request.data['min_value']
        max_value = request.data['max_value']

        # Call apropriate services method
        question_id = create_numeric_question(
                form_pk,
                text,
                ordinal,
                explainer,
                variable_name,
                is_mandatory,
                is_integer,
                min_value,
                max_value
            )
        # Return question id
        return question_id


class FormQuestionsDetail(APIView):
    """Create django rest form questions list."""

    def delete(self, request, form_pk, pk):
        """Delete a question based on its ID."""

        # Extract relevant data from http request
        # Django automatically extracts the pk
        # from the url pattern, so nothing to do here.

        # Call apropriate services method
        try:
            delete_question(pk)
        except Question.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
                )
        # Create response via empty JSON object
        response = {
        }
        # Return response
        return Response(response)

    def put(self, request, form_pk, pk):
        """Update a question based on its ID."""

        # Validate common required attributes
        common_attributes = [
            'text',
            'ordinal',
            'explainer',
            'is_mandatory',
            'type',
        ]
        for attribute in common_attributes:
            if attribute not in request.data.keys():
                return Response(
                    {
                        'error': 'Invalid request. Please supply ' + attribute
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Extract relevant informaiton from JSON object into set of variables
        text = request.data['text']
        ordinal = request.data['ordinal']
        explainer = request.data['explainer']
        is_mandatory = request.data['is_mandatory']

        # Call the apropriate post method depending on Q type,
        # using switch statement
        try:
            match request.data['type']:
                case "boolean":
                    question_id = update_boolean_question(
                        pk,
                        text,
                        ordinal,
                        explainer,
                        is_mandatory
                    )

                case "numeric":
                    question_id = self.__put_numeric_question(
                        request,
                        form_pk,
                        pk,
                        text,
                        ordinal,
                        explainer,
                        is_mandatory
                    )

                case "multiple_choice":
                    question_id = update_multiple_choice_question(
                        pk,
                        text,
                        ordinal,
                        explainer,
                        is_mandatory
                    )

                case _:
                    return Response(
                        {
                            'error': 'Invalid request. Type should be' +
                            ' boolean, numeric or multiple_choice'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
        except ValidationError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except IntegrityError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Form.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        except MultipleChoiceQuestion.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        except BooleanQuestion.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        except NumericQuestion.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        except Question.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            'id': question_id
        })

    # Method to put Numeric question
    def __put_numeric_question(
        self,
        request,
        form_pk,
        pk,
        text,
        ordinal,
        explainer,
        is_mandatory
    ):
        """Update a numeric question specifically."""

        # Validate that the specific attributes required are presnet
        specific_attributes = [
            'is_integer',
            'min_value',
            'max_value',
        ]
        for attribute in specific_attributes:
            if attribute not in request.data.keys():
                return Response(
                    {
                        'error': 'Invalid request. Please supply ' + attribute
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Extract specific attributes from JSON data
        is_integer = request.data['is_integer']
        min_value = request.data['min_value']
        max_value = request.data['max_value']

        # Call apropriate services method
        update_numeric_question(
            pk,
            text,
            ordinal,
            explainer,
            is_mandatory,
            is_integer,
            min_value,
            max_value
        )


class MultipleChoiceOptionsList(APIView):
    """Create django rest multiple choice option list view."""

    def post(self, request, form_pk, question_pk):
        """Create a new multiple choice option."""

        # Validate common required attributes
        common_attributes = [
            'text',
            'explainer',
        ]
        for attribute in common_attributes:
            if attribute not in request.data.keys():
                return Response(
                    {
                        'error': 'Invalid request. Please supply ' + attribute
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Extract relevant informaiton from JSON object into set of variables
        text = request.data['text']
        explainer = request.data['explainer']

        # Call the apropriate post method depending on Q type, using switch
        # statement
        try:
            option_id = create_multiple_choice_option(
                question_pk,
                text,
                explainer
            )
        except ValidationError as e:
            print(str(e))
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except IntegrityError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except MultipleChoiceQuestion.DoesNotExist as e:
            print(str(e))
            return Response(
                status=status.HTTP_404_NOT_FOUND
                )
        if option_id == 0:
            print('Question ID == 0')
            return Response(
                {
                    'error': 'Invalid request. Please supply all required' +
                    ' attributes'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({
            'option_id': option_id
        })


class MultipleChoiceOptionDetail(APIView):
    """Create multiple choice option detail view."""

    def delete(self, request, form_pk, question_pk, pk):
        """Delete a multiple choice option based on its id."""

        # Call apropriate services method
        try:
            delete_multiple_choice_option(pk)
        except MultipleChoiceOption.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
                )
        # Create response via empty JSON object
        response = {}
        # Return response
        return Response(response)
