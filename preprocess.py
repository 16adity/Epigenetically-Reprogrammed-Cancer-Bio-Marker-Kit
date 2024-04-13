import os
from sklearn.model_selection import train_test_split

# Assuming your dataset is in a folder named "blood_cancer"
data_dir = 'C:\\Users\\asus\\Desktop\\cancer new\\Blood_Cancer'

# Get a list of image filenames
image_files = [f for f in os.listdir(data_dir) if f.endswith('.tiff')]

# Assuming the labels are binary (cancer or non-cancer)
labels = [1] * len(image_files)  # Set all labels to 1 (cancer)

# Split the data into training, validation, and test sets
train_images, test_images, train_labels, test_labels = train_test_split(image_files, labels, test_size=0.2, random_state=42)
val_images, test_images, val_labels, test_labels = train_test_split(test_images, test_labels, test_size=0.5, random_state=42)

# Create directories for the sets
train_dir = os.path.join(data_dir, 'train')
val_dir = os.path.join(data_dir, 'val')
test_dir = os.path.join(data_dir, 'test')

os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Move images to the respective directories
for img, label in zip(train_images, train_labels):
    os.rename(os.path.join(data_dir, img), os.path.join(train_dir, img))

for img, label in zip(val_images, val_labels):
    os.rename(os.path.join(data_dir, img), os.path.join(val_dir, img))

for img, label in zip(test_images, test_labels):
    os.rename(os.path.join(data_dir, img), os.path.join(test_dir, img))
