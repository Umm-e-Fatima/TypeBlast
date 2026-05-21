import random # Import the random module from the standard library

class TextBank: # Define the TextBank class to store typing practice texts
    PARAGRAPHS = [ # Initialize a class-level list called PARAGRAPHS with exactly 5 items
        "The rapid evolution of artificial intelligence is changing how we interact with data.", # Technology topic paragraph
        "Countless stars illuminate the vast darkness of the universe, hiding unknown worlds.", # Space topic paragraph
        "Tall pine trees swayed gently in the mountain breeze as the golden sun began to set.", # Nature topic paragraph
        "Writing clean and efficient code requires continuous practice and attention to details.", # Programming topic paragraph
        "The Great Wall of China is one of the most impressive architectural feats in history." # General knowledge topic paragraph
    ] # Close the PARAGRAPHS list definition

    @classmethod # Decorate the following method as a class method
    def get_random(cls): # Define the get_random class method taking 'cls'
        return random.choice(cls.PARAGRAPHS) # Return a random paragraph using random.choice

    @classmethod # Decorate the following method as a class method
    def get_all(cls): # Define the get_all class method taking 'cls'
        return cls.PARAGRAPHS # Return the full list of paragraphs
