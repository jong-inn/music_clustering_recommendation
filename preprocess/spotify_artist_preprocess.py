import json

# Set the numbers to be used to loop over extracted artist files
x = 0
y = 100

# Loop to go through all extracted mpd files
while y <= 1000:
    # Read the json file
    with open("artists.extracted.mpd.slice." + str(x) + "-" + str(y) + ".json", "r") as json_file:
        data = json_file.read()
        content = json.loads(data)

    # Define 3 items to be removed from the json
    items_to_removed = ["external_urls", "followers", "images", "href", "type"]

    # Iterate through all the key.value pair of dictionary
    for key, item in content.items():
        for item_to_remove in items_to_removed:
            # Remove the item
            content[key].pop(item_to_remove)

    # Write the processed data into new json file
    with open("artists.preprocessed_data." + str(x) + "-" + str(y) + ".json", "w") as outfile:
        json.dump(content, outfile)

        x += 100
        y += 100
