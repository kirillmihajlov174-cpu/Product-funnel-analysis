# Business conclusions

## What was analyzed
A synthetic dataset of **5,000 users** for an investment app was used.
The funnel includes 5 stages:

1. Landing viewed
2. Signed up
3. KYC completed
4. Deposit made
5. First trade

## Key findings
- The biggest relative drop is between **Deposit made** and the previous stage: **42.3%**.
- The strongest acquisition source by deposit conversion is **organic** with **29.3%** of users moving from landing to deposit.
- The weakest acquisition source by deposit conversion is **social_ads** with **19.7%**.
- Social traffic converts noticeably worse than referral and organic traffic, which may indicate lower traffic quality or poor onboarding fit.

## Product hypotheses
1. **KYC friction is too high.** Users may drop because verification takes too long or asks for too many steps.
2. **Deposit is not motivated enough after KYC.** Users finish verification but do not understand the next value step.
3. **Traffic quality differs by source.** Social ads bring colder traffic than referral/organic users.

## Recommendations
1. Simplify the KYC path:
   - reduce steps
   - show clear progress bar
   - save unfinished progress
2. Add post-KYC activation prompts:
   - first deposit bonus
   - tutorial explaining why deposit matters
   - personalized nudges within 24 hours
3. Reallocate marketing budget:
   - scale referral and organic
   - review targeting/creative for social ads
4. Build a follow-up A/B test:
   - test simpler KYC UX
   - measure conversion to deposit and first trade
