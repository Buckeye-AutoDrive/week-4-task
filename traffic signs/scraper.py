from icrawler.builtin import GoogleImageCrawler
import os

def download_images(query, num_images=625, output_directory="./"):
    google_crawler = GoogleImageCrawler(storage={'root_dir': output_directory})

    # Filter to get real-world objects only
    filters = {
        'size': 'medium',  # Filters out small images
        'type': 'photo'  # Filters for photo types only
    }

    # Start the download process
    google_crawler.crawl(
        keyword=query,
        max_num=num_images,
        filters=filters
    )

    # After downloading, we can count the number of files in the output directory
    downloaded_images = os.listdir(output_directory)
    return len(downloaded_images)

def ensure_minimum_images(query, output_directory, min_images=50, additional_images=625):
    current_count = len(os.listdir(output_directory))
    if current_count < min_images:
        # Calculate how many more images are needed
        needed_images = min_images - current_count
        # Download only the needed amount or the additional_images specified, whichever is lower
        num_images_to_download = min(needed_images, additional_images)
        downloaded = download_images(query, num_images=num_images_to_download, output_directory=output_directory)
        print(f"Downloaded {downloaded} additional images for '{query}' to reach the minimum of {min_images}.")

# Define the traffic signs you want to collect
traffic_signs = [
    "yield sign",
    "stop sign",
    "speed limit sign",
    "pedestrian crossing sign",
    "railroad crossing sign",
    "roundabout sign",
    "left turn only sign",
    "right turn only sign",
    "no left turn sign",
    "no right turn sign",
    "do not enter sign",
    "road closed sign",
    "no turn on red sign",
    "no parking sign",
    "handicap parking sign",
    "crosswalk sign"
]

# Download images for each traffic sign and count how many were successfully downloaded
if __name__ == "__main__":
    download_counts = {}  # Dictionary to store counts for each sign type
    total_images = 0

    for sign in traffic_signs:
        sign_folder = f"./{sign.replace(' ', '_')}"  # Create a folder for each sign
        os.makedirs(sign_folder, exist_ok=True)  # Ensure the folder exists

        # Initially download images
        downloaded = download_images(sign, num_images=625, output_directory=sign_folder)
        download_counts[sign] = downloaded  # Store count for each traffic sign
        total_images += downloaded

        # Ensure at least 50 images are present
        ensure_minimum_images(sign, sign_folder)

    # Print individual counts and total
    print("Downloaded image counts for each traffic sign:")
    for sign, count in download_counts.items():
        print(f"{sign}: {count} images")

    print(f"Total images downloaded for all traffic signs: {total_images}")
