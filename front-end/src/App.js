import React from 'react';
import ViewPersons from './components/ViewPersons';

const App = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-600 text-white py-4">
        <h1 className="text-center text-3xl font-bold">Neo4j Persons Management</h1>
      </header>
      <main className="py-8">
        <ViewPersons />
      </main>
    </div>
  );
};

export default App;
