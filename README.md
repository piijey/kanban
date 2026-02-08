# Kanban Board

A simple and intuitive kanban board application with user feedback functionality.

## Features

- ✅ **Drag and Drop**: Easily move tasks between columns (To Do, In Progress, Done)
- 📝 **Task Management**: Add and delete tasks
- 💬 **User Feedback**: Built-in feedback system for bug reports, feature requests, and improvements
- 💾 **Local Storage**: Tasks and feedback are automatically saved in your browser
- 🎨 **Beautiful UI**: Modern, responsive design with smooth animations
- 📊 **Task Counters**: See the number of tasks in each column at a glance

## Getting Started

### Installation

1. Clone the repository:
```bash
git clone https://github.com/piijey/kanban.git
cd kanban
```

2. Open the application:
Simply open `index.html` in your web browser. No build process or dependencies required!

### Usage

#### Managing Tasks

1. **Add a Task**: Click the "+ Add Task" button in any column
2. **Move Tasks**: Drag and drop tasks between columns to update their status
3. **Delete Tasks**: Click the "Delete" button on any task to remove it

#### Providing Feedback

1. Click the "Give Feedback" button in the header
2. Select the feedback type (Bug Report, Feature Request, Improvement, or Other)
3. Enter your feedback and optionally provide your email
4. Submit to save your feedback

## Technology Stack

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations and flexbox/grid layouts
- **Vanilla JavaScript**: No frameworks or libraries required
- **LocalStorage API**: For persistent data storage

## Browser Compatibility

Works on all modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Features in Detail

### Task Columns

The board has three default columns:
- **To Do**: Tasks that need to be started
- **In Progress**: Tasks currently being worked on
- **Done**: Completed tasks

### Feedback System

The feedback system allows users to:
- Report bugs
- Request new features
- Suggest improvements
- Submit other general feedback

All feedback is stored locally and logged to the console (in a production environment, this would be sent to a backend server).

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this project for personal or commercial purposes.