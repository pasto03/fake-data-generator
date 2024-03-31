from openai import OpenAI
import json


def generate_csv(columns:str, nrows:int, OPENAI_API_KEY, model="gpt-3.5-turbo", 
                 max_tokens=512, temperature=0, stream=True):
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = "Columns: {}\n" \
             "Number of results: {} rows".format(columns, nrows)
    if nrows > 30:
        nrows = 30
        print("Maximum number of rows is hard-limited to 30 rows.")

    messages = [
        {"role": "system", "content": "You are an assistant who helps to generate random table data based on" +
                    " user prompt. Only provide csv output."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            stream=stream,
            max_tokens=max_tokens,
            messages=messages,
            temperature=temperature
        )

        return response, messages
    except:
        return "e", ""


def yield_rows(response):
#     outputs = []
    row = ""
    i = 0
    for r in response:
        chunk = r.choices[0].delta.content
        if chunk:
            if chunk == "\n":
#                 outputs.append(row)
                if i != 0:
                    r = {"text": row}
                    yield f"{json.dumps(r)}\n\n"
                else:
                    i += 1
                row = ""
            else:
                row += chunk


if __name__ == "__main__":
    client = OpenAI(api_key="")
    print(client)
    # OPENAI_API_KEY = open("openai_api_key").read()
    # response, messages = generate_csv(columns="name, student_id[7 digit int], email, field_of_study, academic_year[1-4]", 
    #                                   nrows=10, OPENAI_API_KEY=OPENAI_API_KEY, max_tokens=512)
    # for row in yield_rows(response):
    #     print(row)