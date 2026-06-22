# ZoomInfo Marketing Context Repository

This OKF repository was rebuilt from `marketing-main/knowledge-base` for corpus pressure testing.

## Classification rule

Content that maps to a governed marketing construct is stored as a Document. Source material that does not map cleanly to a governed construct is stored as a Collection. Case studies are Documents because `case-study` is a governed construct. Sales calls are Collections because call transcripts are supporting evidence, not a governed construct.

## Document areas

- `brand/` contains brand messaging and legal/compliance language from the brand guidelines.
- `voice/` contains writing, linking, and content production rules.
- `audiences/` contains ICP and audience-profile Documents.
- `case-studies/` contains customer case-study Documents.
- `products/` contains product/offering rollups.
- `competitors/` contains competitive landscape Documents.
- `proof/` contains proof-point and advocacy context.
- `measurement/` contains SEO and measurement context.

## Collections

- `sales-call-transcripts` contains raw call transcript and pain-point source files. Audience-profile Documents declare this Collection as supporting evidence.
- `knowledge-base-source-metadata` contains non-construct operational files such as schema, logs, README, and crawl CSV metadata.
