# flaky-test-detective

Parse JUnit XML from multiple runs and identify tests that both pass and fail.

```powershell
python -m pip install -e .
flaky-test-detective report fixtures/run1.xml fixtures/run2.xml
flaky-test-detective report "fixtures/*.xml" --format json
```

A result is intermittent when a normalized test identifier has at least one pass
and one fail across all non-skipped observations. `flake_rate` is
`fail_count / (pass_count + fail_count)`; it is an observed proportion, not a
probability estimate. Skipped runs are reported but excluded from that rate.
