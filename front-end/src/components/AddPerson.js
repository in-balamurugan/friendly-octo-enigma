import React, { useState } from 'react';
import axios from 'axios';

const AddPerson = () => {
  const [name, setName] = useState('');
  const [dateOfBirth, setDateOfBirth] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/add_person/', {
        name,
        dateOfBirth,
      });
      setMessage(response.data.status);
      setName('');
      setDateOfBirth('');
    } catch (error) {
      setMessage('Error: ' + error.response.data.detail);
    }
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Add Person</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium">Name:</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="mt-1 p-2 block w-full border rounded-md"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium">Date of Birth:</label>
          <input
            type="date"
            value={dateOfBirth}
            onChange={(e) => setDateOfBirth(e.target.value)}
            className="mt-1 p-2 block w-full border rounded-md"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-md"
        >
          Add Person
        </button>
      </form>
      {message && <p className="mt-4 text-center">{message}</p>}
    </div>
  );
};

export default AddPerson;
