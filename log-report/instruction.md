There is an access log at /app/access.log, in standard Apache combined log format
(one request per line, client IP first, quoted request method and path in the
middle).

Parse the log and write a JSON report to /app/report.json with exactly these
three keys:

1. total_requests — an integer, the number of log lines (requests) in the file.
2. unique_ips — an integer, the number of distinct client IP addresses that
   appear in the log.
3. top_path — a string, the request path (e.g. "/index.html") that appears
   most often across all requests. If there's a tie, any of the tied paths
   is acceptable.

The file must be valid JSON and must live at exactly /app/report.json.
