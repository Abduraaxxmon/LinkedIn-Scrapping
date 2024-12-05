import pandas as pd
import os


def collect_into_dataframe(name_companies, job_titles, location_jobs, post_dates, skills, sources, logo_urls,country,job,file_name_skills):
    country_list = [country] * len(name_companies)
    job_title_from_list=[job]*len(name_companies)
    salary_list=["NaN"]*len(name_companies)
    # ID,Posted_date,Job Title from List,Job Title,Company,Company Logo URL,Country,Location,Skills,Salary Info,Source
    data = {
        "id":range(1,len(name_companies)+1),
        "Posted_date": post_dates,
        "Job Title from List": job_title_from_list,
        "Job Title": job_titles,
        "Company": name_companies,
        "Company Logo URL": logo_urls,
        "Country": country_list,
        "Location": location_jobs,
        "Salary": salary_list,
        "Skills": skills,
        "Source": sources,
    }

    # Convert the dictionary into a DataFrame
    df = pd.DataFrame(data)
    file_name_skills = f"{file_name_skills} skills"
    create_skills_cross_join_csv(jobs_df=df, file_name=file_name_skills,folder_name="Skills data")

    return df




def save_dataframe_to_csv(df, file_name, folder_name="data"):
    try:

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        file_name_csv=f"{file_name}.csv"
        # Construct the full file path
        file_path = os.path.join(folder_name, file_name_csv)

        # Save the DataFrame to the specified path
        df.to_csv(file_path, index=False)
        print(f"DataFrame successfully saved to {file_path}")

    except Exception as e:
        print(f"An error occurred while saving the DataFrame: {e}")



def create_skills_cross_join_csv(jobs_df, file_name, folder_name="data"):

    try:
        # Prepare an empty list for the expanded rows
        expanded_rows = []

        # Iterate over each job row
        for _, row in jobs_df.iterrows():
            skills_list = row['Skills'].split(', ')  # Split skills string into a list
            for skill in skills_list:
                expanded_row = {
                    "Posted_date": row["Posted_date"],
                    "Job Title": row["Job Title"],
                    "Country": row["Country"],
                    "Company": row["Company"],
                    "Skill": skill
                }
                expanded_rows.append(expanded_row)

        # Convert the expanded rows into a DataFrame
        expanded_df = pd.DataFrame(expanded_rows)

        # Save the expanded DataFrame to a CSV file
        save_dataframe_to_csv(expanded_df, file_name, folder_name)
    except Exception as e:
        print(f"An error occurred during the skills cross-join process: {e}")

# Function to translate text to English
