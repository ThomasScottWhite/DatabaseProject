import React, { useState } from 'react';
import { Card, Container, Row, Col, Button } from 'react-bootstrap';

const Members = () => {
    const [members] = useState([
        { id: 1, name: 'John Doe', role: 'President', email: 'john@example.com' },
        { id: 2, name: 'Joe Smith', role: 'Vice President', email: 'joe@example.com' },
        { id: 3, name: 'Mike Johnson', role: 'Member', email: 'mike@example.com' },
        { id: 4, name: 'Jack Davis', role: 'Member', email: 'jack@example.com' },
    ]);

    return (
        <Container className="mt-5">
            <h2 className="text-center mb-4">Organization Members</h2>
            <Row>
                {members.map((member) => (
                    <Col xs={12} md={6} lg={4} key={member.id} className="mb-4">
                        <Card>
                            <Card.Body>
                                <Card.Title>{member.name}</Card.Title>
                                <Card.Subtitle className="mb-2 text-muted">{member.role}</Card.Subtitle>
                                <Card.Text>Email: {member.email}</Card.Text>
                                <Button variant="primary">View Profile</Button>
                            </Card.Body>
                        </Card>
                    </Col>
                ))}
            </Row>
        </Container>
    );
};

export default Members;
