import json
from collections import defaultdict

# Function to organize apps by platform, software type, and requirement type, including subdomains
def organize_apps(data):
    # Defaultdict for platforms and software types
    organized_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))

    for subdomain in data.get("Subdomains", []):
        subdomain_name = subdomain.get("Subdomain Name", "Unknown Subdomain")
        for region in subdomain.get("Regions", []):
            for app in region.get("Apps", []):
                app_name = app["name"]

                # Handle Functional Requirements (FR)
                functional_requirements = app.get("functional_requirements", {})
                for platform, layers in functional_requirements.items():
                    for layer, features in layers.items():
                        for feature in features:
                            # Ensure the feature already exists or create it
                            feature_exists = False
                            for item in organized_data[subdomain_name][platform][layer]["FR"]:
                                if item["Feature"] == feature:
                                    item["apps"].append(app_name)
                                    feature_exists = True
                                    break
                            if not feature_exists:
                                organized_data[subdomain_name][platform][layer]["FR"].append({
                                    "Feature": feature,
                                    "apps": [app_name]
                                })

                # Handle Non-Functional Requirements (NFR)
                non_functional_requirements = app.get("non_functional_requirements", {})
                for platform, layers in non_functional_requirements.items():
                    for layer, features in layers.items():
                        for feature in features:
                            # Ensure the feature already exists or create it
                            feature_exists = False
                            for item in organized_data[subdomain_name][platform][layer]["NFR"]:
                                if item["Feature"] == feature:
                                    item["apps"].append(app_name)
                                    feature_exists = True
                                    break
                            if not feature_exists:
                                organized_data[subdomain_name][platform][layer]["NFR"].append({
                                    "Feature": feature,
                                    "apps": [app_name]
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
    input_file = "metaapp_data.json"  # Ensure this file exists in the same directory
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
                    for feature in features:
                        print(f"        - {feature['Feature']}: {feature['apps']}")
