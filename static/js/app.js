var Message = React.createClass({
    render: function () {
        return (
            <div className="message">
                <img src={this.props.message.user.avatar} />
                {this.props.message.ts}
                <strong>{this.props.message.user.name}</strong>: {this.props.message.raw}
            </div>
        );
    }
});

var MessageList = React.createClass({
    render: function () {
        var messageNodes = this.props.data.map(function(message) {
            return (
                <Message message={message} />
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
    loadMessages: function(before_message) {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            data: { before_message: before_message },
            success: function(data) {
                Array.prototype.push.apply(data, this.state.data);
                this.setState({data: data});
            }.bind(this)
        });
    },
    handleLoadMore: function() {
        this.loadMessages(this.state.data[0]['id']);
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
            <div onClick={this.handleLoadMore}>Load more</div>
            <MessageList data={this.state.data} />
        </div>
    }
});

ReactDOM.render(
    <MessageBox url="/messages/" />,
    document.getElementById('container')
);
