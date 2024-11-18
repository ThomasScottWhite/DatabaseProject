import React, { useState, useEffect } from 'react';
import { Table, Container } from 'react-bootstrap';

const ViewBills = () => {
    // Dummy data for bills
    const [bills, setBills] = useState([
        { invoicee_id: 1, bill_name: 'Chapter Rent', amount: 1000, date: '2024-10-30', invoicee_name: "Joe" },
        { invoicee_id: 2, bill_name: 'Greek Markup', amount: 500, date: '2024-11-05', invoicee_name: "Joe" },
        { invoicee_id: 3, bill_name: 'Parking (we are evil)', amount: 30, date: '2024-10-28', invoicee_name: "Joe" },
    ]);    
    const payload = { someKey: 'someValue' };

    const Refresh = async () => {
        try {
            const response = await fetch('/api/outgoing-bills', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            setBills(data.bills);

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    useEffect(() => {
        Refresh();
    }, []);


    return (
        <Container className="mt-5">
            <h2 className="text-center mb-4">Outgoing Bills</h2>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Invoicee</th>
                        <th>Bill Name</th>
                        <th>Amount ($)</th>
                        <th>Due Date</th>

                    </tr>
                </thead>
                <tbody>
                    {bills.map((bill) => (
                        <tr key={bill.invoicee_id}>
                            <td>{bill.invoicee_id}</td>
                            <td>{bill.invoicee_name}</td>
                            <td>{bill.bill_name}</td>
                            <td>{bill.amount}</td>
                            <td>{bill.date}</td>

                        </tr>
                    ))}
                </tbody>
            </Table>
        </Container>
    );
};

export default ViewBills;
