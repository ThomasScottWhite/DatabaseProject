import React, { useState, useEffect } from "react";
import { Table, Container, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { useUser } from "../context/user_context";

const ViewBills = () => {
  const [bills, setBills] = useState(null); // Initialize with null to indicate loading state
  const user = useUser();
  const navigate = useNavigate();

  const Refresh = async () => {
    try {
      const memberEmail = user.user.email; // Get the member email from user context
      const response = await user.get_with_headers(
        `/api/member/${memberEmail}/bills`
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setBills(data); // Directly set the fetched data
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    Refresh();
  }, []);

  const handlePay = (bill) => {
    navigate(`/payment/${bill.bill_id}/${bill.amount}/${bill.desc}`);
  };

  if (bills === null) {
    return (
      <Container className="mt-5">
        <h2 className="text-center mb-4">Loading Bills...</h2>
      </Container>
    );
  }

  return (
    <Container className="mt-5">
      <h2 className="text-center mb-4">View Bills</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>#</th>
            <th>Bill Id</th>
            <th>Description</th>
            <th>Amount ($)</th>
            <th>Due Date</th>
            <th>Issue Date</th>
            <th>Source</th>
            <th>Paid</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {bills.map((bill, index) => (
            <tr key={bill.bill_id}>
              <td>{index + 1}</td>
              <td>{bill.bill_id}</td>
              <td>{bill.desc}</td>
              <td>{bill.amount}</td>
              <td>{new Date(bill.due_date).toLocaleDateString()}</td>
              <td>{new Date(bill.issue_date).toLocaleDateString()}</td>
              <td>{bill.is_external ? "External" : "Internal"}</td>
              <td>{bill.amount_paid > 0 ? "Yes" : "No"}</td>
              <td>
                {bill.amount_paid === 0 && (
                  <Button variant="success" onClick={() => handlePay(bill)}>
                    Pay
                  </Button>
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
