const express = require('express');
const app = express();
app.use(express.json());

// Root route (to handle "/")
app.get('/', (req, res) => {
    res.send('Welcome to the Calculator API! Use /add to perform calculations.');
});

// GET method for /add
app.get('/add', (req, res) => {
    const num1 = parseFloat(req.query.num1);
    const num2 = parseFloat(req.query.num2);
    const sum = num1 + num2;
    res.send(`Sum is ${sum}`);
});

// POST method for /add
app.post('/add', (req, res) => {
    const { num1, num2 } = req.body;
    const sum = num1 + num2;
    res.send(`Sum is ${sum}`);
});

// Set port to 8080 (or the port provided by Elastic Beanstalk)
const port = process.env.PORT || 8080;
app.listen(port, () => console.log(`Server running on port ${port}`));
