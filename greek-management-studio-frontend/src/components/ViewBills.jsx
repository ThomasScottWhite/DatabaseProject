import React, { useState } from 'react';
import { Table, Container, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const ViewBills = () => {
    const [bills, setBills] = useState([
        { id: 1, name: 'Chapter Rent', amount: 1000, dueDate: '2024-10-30', source: "Example", paid: false },
        { id: 2, name: 'Greek Markup', amount: 500, dueDate: '2024-11-05', source: "Example", paid: false },
        { id: 3, name: 'Parking (we are evil)', amount: 30, dueDate: '2024-10-28', source: "Example", paid: false },
    ]);

    const navigate = useNavigate();

    const handlePay = (bill) => {
        navigate('/payment', { state: { bill } });
    };

    return (
        <Container className="mt-5">
            <h2 className="text-center mb-4">View Bills</h2>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Bill Name</th>
                        <th>Amount ($)</th>
                        <th>Due Date</th>
                        <th>Source</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {bills.map((bill) => (
                        <tr key={bill.id}>
                            <td>{bill.id}</td>
                            <td>{bill.name}</td>
                            <td>{bill.amount}</td>
                            <td>{bill.dueDate}</td>
                            <td>{bill.source}</td>
                            <td>{bill.paid ? 'Paid' : 'Unpaid'}</td>
                            <td>
                                {!bill.paid ? (
                                    <Button variant="success" onClick={() => handlePay(bill)}>
                                        Pay
                                    </Button>
                                ) : (
                                    'Paid'
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </Container>
    );
};

export default ViewBills;
