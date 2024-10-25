import React, { useState } from 'react';
import { Table, Container } from 'react-bootstrap';

const ViewBills = () => {
    // Dummy data for bills
    const [bills] = useState([
        { id: 1, name: 'Chapter Rent', amount: 1000, dueDate: '2024-10-30', Source: "Joe" },
        { id: 2, name: 'Greek Markup', amount: 500, dueDate: '2024-11-05', Source: "Joe" },
        { id: 3, name: 'Parking (we are evil)', amount: 30, dueDate: '2024-10-28', Source: "Joe" },
    ]);

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
                        <tr key={bill.id}>
                            <td>{bill.id}</td>
                            <td>{bill.Source}</td>
                            <td>{bill.name}</td>
                            <td>{bill.amount}</td>
                            <td>{bill.dueDate}</td>

                        </tr>
                    ))}
                </tbody>
            </Table>
        </Container>
    );
};

export default ViewBills;
