import React from "react";
import './App.css';
import LineChart from "./components/LineChart";


class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            items: [],
            tbdata: [],
            DataisLoaded: false
        };
    }
    componentDidMount() {
        fetch("/static/data.json")
            .then((res) => res.json())
            .then((json) => {
                this.setState({
                    items: json,
                    DataisLoaded: false
                });
            })
        fetch("/static/table_data.json")
            .then((res) => res.json())
            .then((json) => {
                this.setState({
                    tbdata: json,
                    DataisLoaded: true
                });
            })
    }

    render() {
        const { DataisLoaded, items, tbdata } = this.state;

        if (!DataisLoaded) return <div><h1> Pleses wait some time.... </h1></div>;
        return (
        <div className = "App">
            <div className = 'chart'>
                <LineChart chartData={items} />
            </div>
            <div className = 'tables_data'>
                <table className = 'order_data' id = 'total' >
                    <tr><th><h1>TOTAL</h1></th></tr>
                    <tr><td>{window.token}</td></tr>
                </table>
                <table className = 'order_data'>
                    <tr>
                        <th>№</th>
                        <th>Заказ №</th>
                        <th>Стоимость, $</th>
                        <th>Срок поставки</th>
                    </tr>
                    {tbdata.map((item) => (
                    <tr>
                        <td>{ item.id_row }</td>
                        <td>{ item.id_order }</td>
                        <td>{ item.price_usd }</td>
                        <td>{ item.year }</td>
                    </tr>
                    ))}
                </table>
            </div>
        </div>
        );
    }
}

export default App;