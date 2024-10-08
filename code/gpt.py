# %%
from openai import OpenAI
from dotenv import load_dotenv
import json
import pandas as pd

# os.chdir("./code")
load_dotenv("./.env")

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4-turbo",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Give me 10 ideas for a YouTube channel about Python, please provide the response in JSON. Provide a title and a description for every video, called 'title' and 'description' and store them in dictionary videos"},
  ]
)

output = response.choices[0].message.content
print(output)
# %%
output_json = json.loads(output)
videos = output_json['videos']

df = pd.DataFrame(videos)
df.to_excel("videos.xlsx")

# %%
# Load the CSV file containing initial data
df = pd.read_csv("../results/formA_associations_50_matches.csv")
temp_dict = df.set_index(df.columns[0]).T.to_dict('list')
# Define a function to query the GPT API
def query_gpt(k, v):
    data = ", ".join(v)
    response = client.chat.completions.create(

        model="gpt-4-turbo",
        response_format={"type": "text"},
        messages=[
            {"role": "system", "content": "You are an expert in health, genetics, and nutrition."},
            {"role": "user", "content": f"""Find top 5 matches for {k} from {data}. Give your response in this exact format: 
    'match 1, match 2, ..., match 5'. Don't include any other information.
    Examples of accurate matches: for 'Energy in kcal, from 24hr recall food and supplement intake',
    it could be 'Energy expenditure (24h)',
    'Energy intake',
    'Basal metabolic rate (UKB data field 23105)',
    'Resting metabolic rate',
    'Dietary macronutrient intake.'"""},
        ]
    )
    return response.choices[0].message.content

# Iterate over each row in the DataFrame
result = {}
for count, (k, v)in enumerate(temp_dict.items()):
    matches = query_gpt(k, v)
    print(matches)
    result[k] = matches.split(", ")
    if count == 25:
        break 
print(result)
# %%
# Convert results to a DataFrame
results_df = pd.DataFrame.from_dict(result, orient='index')
results_df.to_csv("../results/gpt_test_matches.csv")

print("Process completed. Top 5 matches for each row have been stored.")
# # %%
# result["Maternal body mass index (BMI) at gestational week 26 GUSTO visit, calculated from weight and height at pw26 visit"]
# %%
