var Router = ReactRouter.Router;
var Route = ReactRouter.Route;
var IndexRedirect = ReactRouter.IndexRedirect;
var browserHistory = ReactRouter.browserHistory;

var Message = React.createClass({
    rawMarkup: function() {
        return { __html: slackdown.parse(this.props.message.text) };
    },
    render: function () {
        return (
            <div className="message">
                <div className="avatar">
                    <img src={this.props.message.user.avatar} />
                </div>
                <div className="content">
                    <div className="header">
                        <span className="username">{this.props.message.user.name}</span>
                        <span className="ts">{this.props.message.ts}</span>
                    </div>
                    <div className="text" dangerouslySetInnerHTML={this.rawMarkup()} />
                </div>
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
        var url = '/messages/' + this.props.params.channel;
        $.ajax({
            url: url,
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
            <div className="load-more-button" onClick={this.handleLoadMore}>Load more</div>
            <MessageList data={this.state.data} />
        </div>
    }
});

ReactDOM.render(
    <Router history={browserHistory}>
        <Route path="/">
            <IndexRedirect to="channel/general" />
            <Route path="channel/:channel" component={MessageBox} />
        </Route>
    </Router>,
    document.getElementById('container')
);
