
# HTTP Overview

HTTP is an application layer protocol and is the foundation of communication for the World Wide Web. HTTP is based on a client/server computing model, where the client (for example, a web browser) and the server (for example, a web server) use a request-response message format to transfer information.

HTTP operates at the Application layer of the TCP/IP model. HTTP presumes a reliable underlying transport layer protocol, so TCP is used.

By default, HTTP is a stateless (or connectionless) protocol; it works without the receiver retaining any client information, and each request can be understood in isolation, without the knowledge of any commands that came before it. HTTP does have some mechanisms, namely HTTP headers, to make the protocol behave as if it were stateful.

The information is media-independent. Any type of data can be sent by HTTP, as long as both the client and the server know how to handle the data content.


Request-Response Cycle
The data is exchanged via HTTP requests and HTTP responses, which are specialized data formats used for HTTP communication. A sequence of requests and responses is called an HTTP session and is initiated by a client by establishing a connection to the server.


Process of the request-response cycle:

Client sends an HTTP request to the web.

Server receives the request.

Server processes the request.

Server returns an HTTP response.

Client receives the response.

You can observe this request-response cycle if you enter the developer mode in your browser, visiting a website and analyzing the HTTP requests and responses shown in network section.


Follow these steps to inspect the request-response cycle.

Visit a URL in the browser.

Enter the developer mode (usually the F12 key).

Select an HTTP session.

Check out the request and response headers.

Inspect the header data.

Inspect the response body data.

HTTP Request
An HTTP request is the message sent by the client. The request consists of four parts:

Request-line, which specifies the method and location of accessing the resource. It consists of the request method (or HTTP verb), request Universal Resource Identifier (URI), and protocol version, in that order.

Zero or more HTTP headers. These contain additional information about the request target, authentication, taking care of content negotiation, and so on.

Empty line, indicating the end of the headers.

Message body, which contains the actual data transmitted in the transaction. It is optional and mostly used in HTTP POST requests.

HTTP requests do have some constraints. They are limited in size and URL length and will return an error if the size is exceeded. While the HTTP standard itself does not dictate any limitations, they are imposed by the specific server configuration. Very long URLs (more than 2048 characters) and big headers (more than 8 KB) should be avoided.

Request body sizes vary and depend on the server and method type, but it is not unusual to use a size of anywhere from a few megabytes to a few gigabytes. Body size is determined from the request headers, specifying the content length and encoding.


The example shows an HTTP request where the client sends the server data to create/update a resource identified with the name Joe.

HTTP Response
An HTTP response is the reply to the HTTP request and is sent by the server. The structure is similar to that of the request and consists of the following parts:

Status-line, which consists of the protocol version, a response code (called HTTP Response Code), and a human-readable reason phrase that summarizes the meaning of the code.

Zero or more HTTP headers. These contain additional information about the response data.

Empty line, indicating the end of the headers.

Message body, which contains the response data transmitted in the transaction.

Example of an HTTP response to a request for a customer named Joe.


HTTP URL
HTTP requests use an URL to identify and locate the resources targeted by the request. The "resource" term in the URL is very broadly defined, so it can represent almost anything—a simple web page, an image, a web service, or something else.


URLs are composed from predefined URI components:

Scheme: Each URL begins with a scheme name that refers to a specification for assigning identifiers within that scheme. Examples of popular schemes are http, https, mailto, ftp, data, and so on.

User info: An optional parameter, it is rarely used in modern web applications due to security risks and has been deprecated.

Host: A URL host can be a fully qualified domain name (FQDN) or an IPv4 or IPv6 public address.

Port: An optional parameter that specifies the connection port. If no port is set, the default port for the scheme is taken (default port is 80 for HTTP).

Resource path: A sequence of hierarchical path segments, separated by a slash ( / ). It is always defined, although it may have zero length (for example, https://www.example.com/).

Query: An optional parameter, preceded by the question mark (?) passed to the server that contains a query string of nonhierarchical data.

Fragment: Also an optional parameter, the fragment starts with a hash ( # ) and provides directions to a secondary resource (for example, specific page in a document). It is processed by the client only.

Two commonly mentioned terms in relation to URLs are URNs and URIs:

URI identifies a resource: ../people/alice.

URL also tells where to find it: http://www.example.com/people/alice.

URN identifies a resource using a (made-up) URN scheme: urn:people:names:alice.


A URI is used to unambiguously identify a resource and is a superset of URLs and Uniform Resource Names (URNs), which means that all URNs and URLs are URIs, but not vice versa. While the URI identifies the resource, it does not necessarily tell us where it is located.

A URN is a URI that uses the URN scheme and identifies a resource within a given namespace. Namespace refers to a group of names or identifiers (for example, a file system, network, and so on). URNs do not guarantee the availability of a resource.