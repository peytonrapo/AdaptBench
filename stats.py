import os
import json

# From GPT

def calculate_summary_statistics(folder_path):
    metrics_summary = {
        "chart_data_retries": [],
        "answering_code_retries": [],
        "chart_code_retries": []
    }

    # Traverse all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if file_name.endswith('.json') and os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)
                    metrics = data.get("metadata", {}).get("metrics", {})
                    for metric in metrics_summary.keys():
                        if metric in metrics:
                            metrics_summary[metric].append(metrics[metric])
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in file: {file_name}")

    # Compute summary statistics for each metric
    summary_statistics = {}
    for metric, values in metrics_summary.items():
        if values:
            summary_statistics[metric] = {
                "total": sum(values),
                "average": sum(values) / len(values),
                "min": min(values),
                "max": max(values)
            }
        else:
            summary_statistics[metric] = {
                "total": 0,
                "average": 0,
                "min": None,
                "max": None
            }

    return summary_statistics

# Example usage
folder_path = "experiment_data/modified_question_tuples"
stats = calculate_summary_statistics(folder_path)

print("Summary Statistics:")
for metric, stats_data in stats.items():
    print(f"\nMetric: {metric}")
    for stat, value in stats_data.items():
        print(f"  {stat.capitalize()}: {value}")