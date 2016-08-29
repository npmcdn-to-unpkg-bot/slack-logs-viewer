var Message = React.createClass({
    render: function () {
        return (
            <div className="message">
                <img src={this.props.avatar} />
                <strong>{this.props.user}</strong>: {this.props.text}
            </div>
        );
    }
});

var MessageList = React.createClass({
    render: function () {
        var messageNodes = this.props.data.map(function(message) {
            return (
                <Message avatar={message.user.avatar} user={message.user.name} text={message.raw} />
            );
        });
        return (
            <div className="messageList">
                {messageNodes}
            </div>
        )
    }
});

var MessageBox = React.createClass({
    loadMessages: function() {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            success: function(data) {
                this.setState({data: data});
            }.bind(this)
        });
    },
    getInitialState: function () {
        return {data: []};
    },
    componentDidMount: function() {
        this.loadMessages();
    },
    render: function () {
        return <div className="messageBox">
            <h1>messages</h1>
            <MessageList data={this.state.data} />
        </div>
    }
});

ReactDOM.render(
    <MessageBox url="/messages/" />,
    document.getElementById('container')
);
