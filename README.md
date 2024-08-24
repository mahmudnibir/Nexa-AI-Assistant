
# Nexa AI Assistant

Nexa AI Assistant is a sophisticated voice-activated assistant designed to perform a variety of tasks, including managing media, providing news updates, handling volume controls, and more. This project integrates various Python libraries to offer a versatile and user-friendly experience.

## Features

- **Voice Commands**: Activate and control the assistant using voice commands.
- **Volume Control**: Adjust the system volume with commands to increase, decrease, or set a specific volume level.
- **News Updates**: Fetch and read the latest news headlines.
- **Media Management**: Play, pause, and manage media playback.
- **System Monitoring**: Check disk storage, battery status, and clear the recycle bin.
- **Web Interaction**: Open websites and search queries based on voice commands.
- **Personalization**: Friendly, engaging responses tailored to the user’s preferences.

## Installation

### Prerequisites

- Python 3.12 or higher
- Required Python libraries (listed below)

### Installing Dependencies

To install the required dependencies, use the following command:

```sh
pip install pyttsx3 speech_recognition webbrowser json datetime requests apscheduler psutil random pytz sklearn pycaw
```

### Cloning the Repository

Clone this repository to your local machine using:

```sh
git clone https://github.com/mahmudnibir/Nexa-AI-Assistant.git
```

## Usage

1. **Run the Assistant**: Navigate to the project directory and execute the script.

   ```sh
   python Nexa.py
   ```

2. **Voice Commands**: Use the following voice commands to interact with the assistant:
   - `increase volume` - Increase the system volume.
   - `decrease volume` - Decrease the system volume.
   - `set volume to [number]` - Set the system volume to a specific percentage.
   - `get volume` - Retrieve the current system volume.
   - `play [song/video]` - Play the specified media.
   - `search [query]` - Perform a web search for the specified query.
   - `news` - Get the latest news headlines.

## Configuration

Customize the assistant’s behavior by modifying the `Nexa.py` file or other configuration files as needed.

## Troubleshooting

- **Volume Control Issues**: If you encounter issues with volume control, ensure that the `pycaw` library is installed correctly and the system supports the required interfaces.
- **Dependency Errors**: Make sure all dependencies are installed as listed in the `requirements.txt` file.

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. Ensure your code adheres to the project’s coding standards and passes all tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please contact [your email address] or open an issue on GitHub.
