import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Assuming you have set up the train_dir variable in your preprocessing script
train_dir = 'C:\\Users\\asus\\Desktop\\cancer new\\Blood_Cancer'
val_dir = 'C:\\Users\\asus\\Desktop\\cancer new\\Blood_Cancer'
test_dir = 'C:\\Users\\asus\\Desktop\\cancer new\\Blood_Cancer'


# Create ImageDataGenerators for training, validation, and test sets
train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

# Assuming your images are resized to 224x224 pixels
img_size = (224, 224)

train_generator = train_datagen.flow_from_directory(train_dir, target_size=img_size, batch_size=32, class_mode='binary')
val_generator = val_datagen.flow_from_directory(val_dir, target_size=img_size, batch_size=32, class_mode='binary')
test_generator = test_datagen.flow_from_directory(test_dir, target_size=img_size, batch_size=32, class_mode='binary')

# Create and compile the model
base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')

base_model.trainable = False

model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Assuming you have a variable 'epochs' representing the number of training epochs
epochs = 1  # You can adjust this based on your needs

model.fit(train_generator, epochs=epochs, validation_data=val_generator)

#evaluate
model.evaluate(test_generator)

# Save the trained model
model.save('C:\\Users\\asus\\Desktop\\cancer new\\cancermodel.h5')





