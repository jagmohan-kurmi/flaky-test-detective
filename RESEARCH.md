# Research

## Sources
- JUnit XML de facto format overview: https://llg.cubic.org/docs/junit/
- Apache JMeter JUnit XML format: https://jmeter.apache.org/usermanual/junit.html
- Python XML ElementTree: https://docs.python.org/3/library/xml.etree.elementtree.html
- Microsoft Engineering, flaky test practices: https://learn.microsoft.com/en-us/azure/devops/learn/engineering-notes/testing-a-flaky-test

## Limits
- JUnit XML has no universal schema; this parser reads common `testsuite`, `testcase`,
  `failure`, `error`, and `skipped` elements.
- A single XML can contain nested suites and suites are traversed by descendant cases.
- Identifier normalization removes only whitespace and common iteration/retry suffixes.
  Product-specific parameter encodings may need configuration.
- Skipped tests are not failures and do not enter the observed pass/fail denominator.
- The tool does not prove cause or assign code ownership.
