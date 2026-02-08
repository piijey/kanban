// Task storage
let tasks = JSON.parse(localStorage.getItem('kanbanTasks')) || [];
let feedbackList = JSON.parse(localStorage.getItem('kanbanFeedback')) || [];
let currentColumn = null;
let draggedTask = null;
let taskIdCounter = Date.now();
let feedbackIdCounter = Date.now();

// Initialize the board
document.addEventListener('DOMContentLoaded', () => {
    renderTasks();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Feedback button
    document.getElementById('feedbackBtn').addEventListener('click', openFeedbackModal);
    
    // Add task buttons
    document.querySelectorAll('.add-task-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            currentColumn = e.target.dataset.column;
            openTaskModal();
        });
    });
    
    // Modal close buttons
    document.querySelectorAll('.close').forEach(closeBtn => {
        closeBtn.addEventListener('click', () => {
            closeBtn.closest('.modal').style.display = 'none';
        });
    });
    
    // Close modals when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
        }
    });
    
    // Forms
    document.getElementById('feedbackForm').addEventListener('submit', handleFeedbackSubmit);
    document.getElementById('taskForm').addEventListener('submit', handleTaskSubmit);
    
    // Drag and drop for task columns
    setupDragAndDrop();
}

// Feedback Modal
function openFeedbackModal() {
    document.getElementById('feedbackModal').style.display = 'block';
    document.getElementById('feedbackForm').reset();
}

function handleFeedbackSubmit(e) {
    e.preventDefault();
    
    const feedback = {
        id: ++feedbackIdCounter,
        type: document.getElementById('feedbackType').value,
        text: document.getElementById('feedbackText').value,
        email: document.getElementById('feedbackEmail').value,
        date: new Date().toISOString()
    };
    
    feedbackList.push(feedback);
    localStorage.setItem('kanbanFeedback', JSON.stringify(feedbackList));
    
    document.getElementById('feedbackModal').style.display = 'none';
    showSuccessMessage('Thank you for your feedback!');
    
    // Log feedback to console (in a real app, this would be sent to a server)
    console.log('Feedback submitted:', feedback);
}

// Task Modal
function openTaskModal() {
    document.getElementById('taskModal').style.display = 'block';
    document.getElementById('taskModalTitle').textContent = 'Add New Task';
    document.getElementById('taskForm').reset();
}

function handleTaskSubmit(e) {
    e.preventDefault();
    
    const task = {
        id: ++taskIdCounter,
        title: document.getElementById('taskTitle').value,
        description: document.getElementById('taskDescription').value,
        status: currentColumn,
        createdAt: new Date().toISOString()
    };
    
    tasks.push(task);
    saveTasks();
    renderTasks();
    
    document.getElementById('taskModal').style.display = 'none';
    showSuccessMessage('Task added successfully!');
}

// Task rendering
function renderTasks() {
    // Clear all columns
    document.querySelectorAll('.tasks').forEach(container => {
        container.innerHTML = '';
    });
    
    // Render tasks in their respective columns
    tasks.forEach(task => {
        const taskElement = createTaskElement(task);
        const container = document.getElementById(`${task.status}-tasks`);
        if (container) {
            container.appendChild(taskElement);
        }
    });
    
    // Update task counts
    updateTaskCounts();
}

function createTaskElement(task) {
    const taskEl = document.createElement('div');
    taskEl.className = 'task';
    taskEl.draggable = true;
    taskEl.dataset.taskId = task.id;
    
    const taskTitle = document.createElement('div');
    taskTitle.className = 'task-title';
    taskTitle.textContent = task.title;
    taskEl.appendChild(taskTitle);
    
    if (task.description) {
        const taskDesc = document.createElement('div');
        taskDesc.className = 'task-description';
        taskDesc.textContent = task.description;
        taskEl.appendChild(taskDesc);
    }
    
    const taskActions = document.createElement('div');
    taskActions.className = 'task-actions';
    
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'task-delete';
    deleteBtn.textContent = 'Delete';
    deleteBtn.addEventListener('click', () => deleteTask(task.id));
    
    taskActions.appendChild(deleteBtn);
    taskEl.appendChild(taskActions);
    
    // Add drag event listeners
    taskEl.addEventListener('dragstart', handleDragStart);
    taskEl.addEventListener('dragend', handleDragEnd);
    
    return taskEl;
}

function updateTaskCounts() {
    const counts = {
        'todo': 0,
        'in-progress': 0,
        'done': 0
    };
    
    tasks.forEach(task => {
        if (counts[task.status] !== undefined) {
            counts[task.status]++;
        }
    });
    
    document.querySelectorAll('.column').forEach(column => {
        const status = column.dataset.status;
        const countEl = column.querySelector('.task-count');
        if (countEl && counts[status] !== undefined) {
            countEl.textContent = counts[status];
        }
    });
}

// Drag and Drop
function setupDragAndDrop() {
    document.querySelectorAll('.tasks').forEach(container => {
        container.addEventListener('dragover', handleDragOver);
        container.addEventListener('drop', handleDrop);
        container.addEventListener('dragenter', handleDragEnter);
        container.addEventListener('dragleave', handleDragLeave);
    });
}

function handleDragStart(e) {
    draggedTask = this;
    this.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
}

function handleDragEnd(e) {
    this.classList.remove('dragging');
    document.querySelectorAll('.tasks').forEach(container => {
        container.classList.remove('drag-over');
    });
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    e.dataTransfer.dropEffect = 'move';
    return false;
}

function handleDragEnter(e) {
    this.classList.add('drag-over');
}

function handleDragLeave(e) {
    if (e.target === this) {
        this.classList.remove('drag-over');
    }
}

function handleDrop(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    
    const taskId = parseInt(draggedTask.dataset.taskId);
    const newStatus = this.id.replace('-tasks', '');
    
    // Update task status
    const task = tasks.find(t => t.id === taskId);
    if (task) {
        task.status = newStatus;
        saveTasks();
        renderTasks();
    }
    
    return false;
}

// Task management
function deleteTask(taskId) {
    if (confirm('Are you sure you want to delete this task?')) {
        tasks = tasks.filter(task => task.id !== taskId);
        saveTasks();
        renderTasks();
        showSuccessMessage('Task deleted successfully!');
    }
}

function saveTasks() {
    localStorage.setItem('kanbanTasks', JSON.stringify(tasks));
}

// Utility functions
function showSuccessMessage(message) {
    const msgEl = document.createElement('div');
    msgEl.className = 'success-message';
    msgEl.textContent = message;
    document.body.appendChild(msgEl);
    
    setTimeout(() => {
        msgEl.remove();
    }, 3000);
}
