class Speech:
    def __init__(self, sample, model):
        self.sample_wav = sample
        self.model = model
        self.rate = ""
        self.audio = ""

    def init_model(self):
        #TODO
        # Set up model with whatever is needed



    def get_audio(self):
        #TODO 
        # Get Audio Sample from self.sample
        # Check what rate is reqd
        # Convert to rate if needed
        # Return audio in self.audio
    
    def train_text(self, cue):
        #TODO
        # Get audio from self.sample
        # Run inference using lib functions
        # Print results of training
        # Return if needed

    def speech_to_text(self):
        #TODO
        # Using library, convert audio to text
        # Return output string
