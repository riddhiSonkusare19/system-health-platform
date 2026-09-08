\# Merge Conflict Notes



\## What happened

Two feature branches - develop (via feature/health-service and feature/metrics-service)

and feature/notifier-service - each independently created README.md to document their

own service, without either branch knowing the other had done the same. When merging

feature/notifier-service into develop, Git reported an add/add conflict on README.md

since both branches added the same file with different content and no common ancestor

version to merge from.



\## How it was resolved

Opened README.md, removed the <<<<<<< / ======= / >>>>>>> conflict markers, and

manually combined both versions into a single "Services" section listing all three

services (health, metrics, notifier) instead of picking one side over the other.

Verified no conflict markers remained before staging and committing the merge.

