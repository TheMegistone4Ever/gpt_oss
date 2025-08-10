from utils import send_chat_request

if __name__ == "__main__":
    locally = False
    user_input = "Explain what MXFP4 quantization is."
    system_message = "You are a helpful assistant."

    answer, elapsed_time = send_chat_request(user_input, system_message, not locally)
    print(f"Response:\n{answer}")
    print(f"Elapsed time: {elapsed_time:.4f} seconds")
