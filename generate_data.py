import pathlib
import numpy as np
import pandas as pd

def main():
    out_dir = pathlib.Path(__file__).resolve().parents[1] / "data"
    out_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(42)
    n_users = 5000
    user_ids = np.arange(1, n_users + 1)

    sources = ['organic', 'paid_search', 'social_ads', 'referral', 'email']
    platforms = ['ios', 'android', 'web']
    countries = ['RU', 'KZ', 'BY', 'UZ']

    user_df = pd.DataFrame({
        'user_id': user_ids,
        'source': rng.choice(sources, size=n_users, p=[0.28, 0.24, 0.18, 0.12, 0.18]),
        'platform': rng.choice(platforms, size=n_users, p=[0.35, 0.40, 0.25]),
        'country': rng.choice(countries, size=n_users, p=[0.55, 0.15, 0.12, 0.18]),
        'signup_date': pd.to_datetime('2025-09-01') + pd.to_timedelta(rng.integers(0, 30 * 24 * 60, size=n_users), unit='m')
    })

    base_probs = {
        'visit_to_signup': 0.62,
        'signup_to_kyc': 0.68,
        'kyc_to_deposit': 0.57,
        'deposit_to_trade': 0.63
    }
    source_effects = {
        'organic': [0.04, 0.03, 0.02, 0.03],
        'paid_search': [0.02, 0.01, -0.01, 0.00],
        'social_ads': [-0.03, -0.04, -0.05, -0.02],
        'referral': [0.05, 0.05, 0.04, 0.05],
        'email': [0.01, 0.02, 0.03, 0.04]
    }
    platform_effects = {
        'ios': [0.03, 0.02, 0.02, 0.02],
        'android': [0.00, 0.00, -0.01, 0.00],
        'web': [-0.02, -0.01, 0.01, 0.01]
    }

    events = []
    for _, row in user_df.iterrows():
        uid = row.user_id
        src = row.source
        plat = row.platform
        t = row.signup_date - pd.Timedelta(minutes=int(rng.integers(5, 240)))

        events.append([uid, 'app_open', t, src, plat, row.country, None])
        events.append([uid, 'view_landing', t + pd.Timedelta(minutes=int(rng.integers(1, 20))), src, plat, row.country, None])

        p1 = base_probs['visit_to_signup'] + source_effects[src][0] + platform_effects[plat][0]
        if rng.random() < p1:
            t1 = row.signup_date
            events.append([uid, 'sign_up', t1, src, plat, row.country, None])

            p2 = base_probs['signup_to_kyc'] + source_effects[src][1] + platform_effects[plat][1]
            if rng.random() < p2:
                t2 = t1 + pd.Timedelta(hours=float(rng.uniform(0.3, 72)))
                events.append([uid, 'kyc_completed', t2, src, plat, row.country, None])

                p3 = base_probs['kyc_to_deposit'] + source_effects[src][2] + platform_effects[plat][2]
                if rng.random() < p3:
                    t3 = t2 + pd.Timedelta(hours=float(rng.uniform(0.1, 96)))
                    amount = round(max(500, rng.lognormal(mean=8.1, sigma=0.65)), 2)
                    events.append([uid, 'deposit_success', t3, src, plat, row.country, amount])

                    p4 = base_probs['deposit_to_trade'] + source_effects[src][3] + platform_effects[plat][3]
                    if rng.random() < p4:
                        t4 = t3 + pd.Timedelta(hours=float(rng.uniform(0.2, 48)))
                        volume = round(max(300, rng.lognormal(mean=7.8, sigma=0.7)), 2)
                        events.append([uid, 'first_trade', t4, src, plat, row.country, volume])

    events_df = pd.DataFrame(events, columns=['user_id', 'event_name', 'event_time', 'source', 'platform', 'country', 'value'])
    events_df = events_df.sort_values(['user_id', 'event_time']).reset_index(drop=True)

    user_df[['user_id', 'source', 'platform', 'country', 'signup_date']].to_csv(out_dir / 'users.csv', index=False)
    events_df.to_csv(out_dir / 'events.csv', index=False)

    print("Data generated successfully.")

if __name__ == "__main__":
    main()
