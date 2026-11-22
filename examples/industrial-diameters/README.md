# Which change can you approve before the import?

A supplier sends a replacement drill-bit feed. One display diameter is shorter than before. Another row changes a drill-point angle. These three fictional records show the evidence a catalog manager needs to review each change.

Download the [approved snapshot](approved.csv) and [incoming snapshot](incoming.csv). Run the command from the repository root.

```sh
python3 review.py examples/industrial-diameters/approved.csv examples/industrial-diameters/incoming.csv --field nominal_in --field display_in --field point_deg
```

The comparison reports three rows in each file and two changes. It preserves the original SKU on each row.

| SKU | In the incoming feed | Review decision |
|---|---|---|
| DEMO-21A | Display changes from 0.328125 to 0.3281 in. | Approve the display value if the destination uses four decimal places. Retain 21/64 in. as the nominal size. |
| DEMO-21B | Same 21/64 in. nominal diameter as DEMO-21A. Its point angle remains 135°. | Keep the two SKUs separate. DEMO-21A has a 118° point. |
| DEMO-29C | Point angle changes from 118° to 135°. | Hold this field until the supplier confirms the specification for this exact SKU. The diameter cannot resolve the angle. |

The comparison reports field changes. A reviewer makes the approval decision and can preserve the original value while awaiting evidence.

## Apply the same review to an industrial catalog

HWC's industrial data standards module starts at $3,500 for one named legal entity. The parties specify the fields, licensed edition and permitted internal use in the order. To discuss a fit, send the product family, the fields your team reviews and how many entities will use the rules. A sample export can follow once data-sharing terms are agreed.

[Discuss an industrial license](https://form.jotform.com/263065301224041?q4_textarea2=I%20found%20the%20industrial%20diameter%20example%20on%20GitHub.%20I%20would%20like%20to%20discuss%20the%20industrial%20data%20standards%20license.%20Our%20product%20family%2C%20fields%2C%20and%20number%20of%20legal%20entities%20are%20) · [Review the license order](https://hunterworkflowconsulting.com/enterprise-data-standards-license-order.pdf)
