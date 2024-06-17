import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Network } from 'vis-network/standalone/esm/vis-network';
import { DataSet } from 'vis-data/standalone/esm/vis-data';

const ViewPersons = () => {
  const [network, setNetwork] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/view_persons/');
        const persons = response.data;
        console.log('API call successful:', persons);

        if (!persons || persons.length === 0) {
          console.warn('No data received from API');
          return; // Handle empty data case (optional)
        }

        const nodes = new DataSet(
          persons.map((person, index) => ({
            id: person.from,
            label: person.name ? `<b>${person.from}</b> - ${person.name}` : `<b>${person.from}</b>`, // Handle missing name
          }))
        );

        const edges = new DataSet(
          persons.map((person, index) => ({
            from: person.from,
            to: person.to,
            label: person.relationship,
          }))
        );

        const container = document.getElementById('network');
        const data = { nodes, edges };
        const options = {
          nodes: {
            shape: 'box',
            font: { multi: 'html' },
          },
          edges: {
            arrows: {
              to: {
                enabled: true,
                scaleFactor: 0.5,
              },
            },
            font: {
              align: 'middle',
            },
          },
        };
        const graph = new Network(container, data, options);
        setNetwork(graph);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Persons and Relationships</h2>
      <div id="network" style={{ width: '100%', height: '400px' }}></div>
    </div>
  );
};

export default ViewPersons;
