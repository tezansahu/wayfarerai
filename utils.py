
# The model response contains more than what we want. We only want to retain the text upto the first occurence of "\nUser". 
# If there is no occurrence of this string, we want to retain the entire text.
# Note that the model response can span over multiple line
def process_model_response(model_response):
    model_response = model_response.strip()
    human_response_start_index = model_response.find("\nUser")
    if human_response_start_index == -1:
        return model_response
    else:
        return model_response[:human_response_start_index]