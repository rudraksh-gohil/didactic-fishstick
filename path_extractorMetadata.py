import json
import random

# Load the JSON file
json_file_path = "org_metaapp_data.json"  # Replace with your file path

try:
    with open(json_file_path, "r") as file:
        data = json.load(file)

        # Function to extract unique combinations of features
        def generate_combinations(features, max_combinations=10):
            variations = []
            while len(variations) < max_combinations:
                # Randomly choose 1 to 3 features
                num_features = random.randint(1, 3)
                selected_features = random.sample(features, num_features)

                # Combine details for selected features
                feature_details = {
                    "Features": [],
                    "Available Apps": set(),
                    "Acceptance Criteria": set(),
                    "Common Bugs": set()
                }

                for feature in selected_features:
                    feature_details["Features"].append(feature["Feature"])
                    # Collect unique apps
                    apps = set([app for country_apps in feature["apps"].values() for app in country_apps])
                    # Collect unique acceptance criteria and common bugs
                    acceptance_criteria = set(feature["acceptance_criteria"].get("mobile", []))
                    common_bugs = set(feature["common_bugs"].get("mobile", []))

                    # Update the details
                    feature_details["Available Apps"].update(apps)
                    feature_details["Acceptance Criteria"].update(acceptance_criteria)
                    feature_details["Common Bugs"].update(common_bugs)

                # Ensure the combination is unique
                feature_variation = tuple(sorted(feature_details["Features"]))
                if feature_variation not in [tuple(sorted(var["Features"])) for var in variations]:
                    # Convert sets back to lists and add to variations
                    feature_details["Available Apps"] = list(feature_details["Available Apps"])
                    feature_details["Acceptance Criteria"] = list(feature_details["Acceptance Criteria"])
                    feature_details["Common Bugs"] = list(feature_details["Common Bugs"])
                    variations.append(feature_details)
            return variations

        # Recursive function to traverse the hierarchy
        def traverse_hierarchy(data, path=[]):
            solutions = []
            for key, value in data.items():
                current_path = path + [key]
                if isinstance(value, dict):  # If the value is a dictionary, recurse further
                    solutions += traverse_hierarchy(value, current_path)
                elif isinstance(value, list):  # If the value is a list (FR or NFR features)
                    solutions.append({
                        "Path": current_path[:-1],  # Exclude the last element (FR/NFR)
                        "Requirement Type": current_path[-1],  # The last path element is FR/NFR
                        "Features": value  # Pass the features list
                    })
            return solutions

        # Start traversal from the top-level hierarchy
        all_groups = traverse_hierarchy(data)

        # Process each group to generate variations
        for group in all_groups:
            path = group["Path"]
            requirement_type = group["Requirement Type"]
            features = group["Features"]

            # Generate unique variations
            variations = generate_combinations(features, max_combinations=4)

            # Print results
            subdomain, platform, software_type = path
            print(f"\nSubdomain: {subdomain} -> Platform: {platform} -> Software Type: {software_type} -> Requirement Type: {requirement_type}")
            for idx, variation in enumerate(variations, 1):
                print(f"\nVariation {idx}:")
                print(f"Features: {variation['Features']}")
                print(f"Available Apps: {variation['Available Apps']}")
                print(f"Acceptance Criteria: {variation['Acceptance Criteria']}")
                print(f"Common Bugs: {variation['Common Bugs']}")

except Exception as e:
    print(f"Error processing the JSON file: {e}")
