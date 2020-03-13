import React, { useState, useEffect } from 'react';
import './App.scss';

import axios from 'axios'

function App(props) {

  const [ user, setUser ] = useState({
    id: 'elijah-mckay',
    balance: '',
    transactions: '',
    chain: ''
  })

  const [ isReloading, setIsReloading ] = useState(false)

  useEffect(() => {
    // console.log('check')
    axios.get('http://0.0.0.0:5000/chain')
    .then(res => {
      console.log(res)
      let relevantTransactions = []
      let counter = 0
      console.log('res', res.data.chain.length)
      console.log('user chain', user.chain.length)
      for(let i = user.chain.length; i < res.data.chain.length; i++) {
        counter++;
        if(res.data.chain[i].transactions.length === 1) {
          if(res.data.chain[i].transactions[0].recipient === user.id || res.data.chain[i].transactions.sender === user.id) {
            // console.log('yes')
            relevantTransactions.push(res.data.chain[i].transactions[0])
          }
        } else if(res.data.chain[i].transactions.length > 1){

        }


        // console.log(res.data.chain[i])
      }
      console.log('counter', counter)

      // console.log(relevantTransactions)
      setUser({
        ...user,
        transactions: relevantTransactions,
        // transactions: relevantTransactions.slice(relevantTransactions.length - 10, relevantTransactions.length),
        chain: res.data.chain
        // chain: res.data.chain.slice(res.data.chain.length - 10, res.data.chain.length)
      })
    })
    .catch(err => {
      console.log(err)
    })

    setTimeout(reload, 15000)
  }, [isReloading])

  const changeHandler = (e) => {
    e.preventDefault();

    setUser({
      ...user,
      [e.target.name]: e.target.value
    })
  }

  // setInterval(window.location.reload(), 15000)
  const reload = () => {
    setIsReloading(!isReloading)
  }
  console.log(user.transactions)
  return (
    <div className="App">
      <h1 className="profile">User</h1>
      <ul>
        <li>* Allow the user to enter, save, or change the `id` used for the program</li>
        <li>* Display the current balance for that user</li>
        <li>* Display a list of all transactions for this user, including sender and recipient</li>
      </ul>
      <label className="input-label">User ID</label><br />
      <input
      type="text"
      onChange={changeHandler}
      value={user.id}
      name="id"
      />
      <h3 className="chain">Chain</h3>
        <table>
          <tr>
            <th>Index</th>
            <th>Previous Hash</th>
            <th>Proof</th>
            <th>Timestamp</th>
          </tr>
          {user.chain !== '' ? user.chain.map((t) => (
            <tr>
              <td>{t.index}</td>
              <td>{t.previous_hash}</td>
              <td>{t.proof}</td>
              <td>{t.timestamp}</td>
            </tr>
          )) : null}
        </table>
      <h3 className="transactions">Transactions</h3>
      <table>
        <tr>
          <th>Sender</th>
          <th>Recipient</th>
          <th>Amount</th>
        </tr>
        {user.transactions ? user.transactions.map((t) => (
          <tr>
            <td>{t.sender}</td>
            <td>{t.recipient}</td>
            <td>{t.amount}</td>
          </tr>
        )) : null}
      </table>
    </div>
  );
}

export default App;
