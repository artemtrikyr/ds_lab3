const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 3000;

// Підключення до MongoDB
mongoose.connect('mongodb://localhost:27017/books', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log('Connected to MongoDB'))
.catch(err => console.error('Could not connect to MongoDB', err));

// Налаштування Middleware
app.use(cors());
app.use(bodyParser.json());

app.get('/books', async (req, res) => {
    try {
        const Book = mongoose.model('Book');
        const books = await Book.find({});
        res.json(books);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Маршрут для отримання даних
app.post('/books', async (req, res) => {
    try {
        const { title, price, description, image_url } = req.body;
        const Book = mongoose.model('Book', new mongoose.Schema({
            title: String,
            price: String,
            description: String,
            image_url: String
        }));

        const newBook = new Book({ title, price, description, image_url });
        await newBook.save();
        res.status(201).json({ message: 'Book saved successfully!' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Запуск сервера
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
