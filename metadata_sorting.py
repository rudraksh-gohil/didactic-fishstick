import json
from collections import defaultdict

# Function to organize apps by platform, software type, requirement type, region, and subdomain
def organize_apps(data):
    # Defaultdict for platforms, software types, and regions
    organized_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))

    for subdomain in data.get("Subdomains", []):
        subdomain_name = subdomain.get("Subdomain Name", "Unknown Subdomain")
        for region in subdomain.get("Regions", []):
            region_name = region.get("Region", "Unknown Region")
            for app in region.get("Apps", []):
                app_name = app["name"]

                # Handle Functional Requirements (FR)
                functional_requirements = app.get("functional_requirements", {})
                for platform, layers in functional_requirements.items():
                    for layer, features in layers.items():
                        for feature in features:
                            # Initialize FR list if it doesn't exist
                            if "FR" not in organized_data[subdomain_name][platform][layer]:
                                organized_data[subdomain_name][platform][layer]["FR"] = []

                            # Check if feature already exists, otherwise create a new entry
                            feature_found = False
                            for item in organized_data[subdomain_name][platform][layer]["FR"]:
                                if item["Feature"] == feature:
                                    # Add the app to the corresponding region list
                                    if region_name not in item["apps"]:
                                        item["apps"][region_name] = []
                                    item["apps"][region_name].append(app_name)
                                    feature_found = True
                                    break
                            if not feature_found:
                                # If feature does not exist, create a new one
                                organized_data[subdomain_name][platform][layer]["FR"].append({
                                    "Feature": feature,
                                    "apps": {region_name: [app_name]}
                                })

                # Handle Non-Functional Requirements (NFR)
                non_functional_requirements = app.get("non_functional_requirements", {})
                for platform, layers in non_functional_requirements.items():
                    for layer, features in layers.items():
                        for feature in features:
                            # Initialize NFR list if it doesn't exist
                            if "NFR" not in organized_data[subdomain_name][platform][layer]:
                                organized_data[subdomain_name][platform][layer]["NFR"] = []

                            # Check if feature already exists, otherwise create a new entry
                            feature_found = False
                            for item in organized_data[subdomain_name][platform][layer]["NFR"]:
                                if item["Feature"] == feature:
                                    # Add the app to the corresponding region list
                                    if region_name not in item["apps"]:
                                        item["apps"][region_name] = []
                                    item["apps"][region_name].append(app_name)
                                    feature_found = True
                                    break
                            if not feature_found:
                                # If feature does not exist, create a new one
                                organized_data[subdomain_name][platform][layer]["NFR"].append({
                                    "Feature": feature,
                                    "apps": {region_name: [app_name]}
                                })

    # Convert to a regular dictionary for saving to JSON
    return json.loads(json.dumps(organized_data))

# Save the organized data to a JSON file
def save_to_file(data, filename="organized_data.json"):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

# Load the input data from a JSON file
def load_input_file(filename="input_data.json"):
    with open(filename, "r") as file:
        return json.load(file)

# Load the organized data from a JSON file
def load_organized_data(filename="organized_data.json"):
    with open(filename, "r") as file:
        return json.load(file)

# Main execution
if __name__ == "__main__":
    # Load input data
    input_file = "appdata.json"  # Ensure this file exists in the same directory
    json_data = load_input_file(input_file)

    # Organize and save data
    organized_data = organize_apps(json_data)
    save_to_file(organized_data)

    # Display the organized data (optional)
    loaded_data = load_organized_data()
    for subdomain, platforms in loaded_data.items():
        print(f"Subdomain: {subdomain}")
        for platform, software_types in platforms.items():
            print(f"  Platform: {platform}")
            for software_type, req_types in software_types.items():
                print(f"    Software Type: {software_type}")
                for req_type, features in req_types.items():
                    print(f"      {req_type}:")
                    if isinstance(features, list):
                        for feature in features:
                            print(f"        - {feature['Feature']}: {feature['apps']}")
                    else:
                        print(f"        {req_type} is not in expected format!")
