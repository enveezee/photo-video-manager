# Photo and Video Manager

This project is a cross-platform application for managing photos and videos, featuring non-destructive editing capabilities. Modifications are stored in XML or JSON format, allowing users to maintain the integrity of their original media files while applying various edits.

## Features

- **Photo Management**: Load, edit, and save photos with non-destructive editing.
- **Video Management**: Load, edit, and save videos with non-destructive editing.
- **Non-Destructive Editing**: Edits are stored separately, allowing for easy reversion and modification.
- **Cross-Platform**: Built using Qt6, ensuring compatibility across different operating systems.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/photo-video-manager.git
   ```
2. Navigate to the project directory:
   ```
   cd photo-video-manager
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

## Project Structure

- `src/main.py`: Entry point of the application.
- `src/ui/main_window.ui`: UI layout for the main application window.
- `src/models/`: Contains classes for managing photo and video data.
- `src/controllers/`: Manages interactions between the UI and models.
- `src/editors/`: Provides editing functionalities for photos and videos.
- `src/storage/`: Handles reading and writing of edit metadata in XML and JSON formats.
- `src/utils/`: Utility functions for file operations.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.