import pathlib
import pandas as pd
import matplotlib.pyplot as plt

STAGES = ['view_landing', 'sign_up', 'kyc_completed', 'deposit_success', 'first_trade']
STAGE_LABELS = {
    'view_landing': 'Landing viewed',
    'sign_up': 'Signed up',
    'kyc_completed': 'KYC completed',
    'deposit_success': 'Deposit made',
    'first_trade': 'First trade'
}

def build_funnel(df: pd.DataFrame, group_col: str | None = None) -> pd.DataFrame:
    rows = []
    if group_col is None:
        counts = {s: df.loc[df.event_name.eq(s), 'user_id'].nunique() for s in STAGES}
        prev = None
        start = counts['view_landing']
        for s in STAGES:
            users = counts[s]
            rows.append([
                STAGE_LABELS[s],
                users,
                1.0 if prev is None else users / prev,
                users / start if start else None
            ])
            prev = users
        return pd.DataFrame(rows, columns=['stage', 'users', 'conversion_from_previous', 'conversion_from_start'])

    for group_value, part in df.groupby(group_col):
        counts = {s: part.loc[part.event_name.eq(s), 'user_id'].nunique() for s in STAGES}
        prev = None
        start = counts['view_landing']
        for s in STAGES:
            users = counts[s]
            rows.append([
                group_value,
                STAGE_LABELS[s],
                users,
                1.0 if prev is None else users / prev,
                users / start if start else None
            ])
            prev = users
    return pd.DataFrame(rows, columns=[group_col, 'stage', 'users', 'conversion_from_previous', 'conversion_from_start'])

def main():
    root = pathlib.Path(__file__).resolve().parents[1]
    data_path = root / 'data' / 'events.csv'
    out_dir = root / 'outputs'
    img_dir = out_dir / 'images'
    out_dir.mkdir(exist_ok=True)
    img_dir.mkdir(exist_ok=True)

    events = pd.read_csv(data_path, parse_dates=['event_time'])

    funnel = build_funnel(events)
    funnel['drop_off_from_previous'] = 1 - funnel['conversion_from_previous']
    funnel.to_csv(out_dir / 'funnel_overall.csv', index=False)

    funnel_by_source = build_funnel(events, group_col='source')
    funnel_by_source.to_csv(out_dir / 'funnel_by_source.csv', index=False)

    funnel_by_platform = build_funnel(events, group_col='platform')
    funnel_by_platform.to_csv(out_dir / 'funnel_by_platform.csv', index=False)

    plt.figure(figsize=(9, 5))
    plt.plot(funnel['stage'], funnel['users'], marker='o')
    plt.title('Product funnel: overall')
    plt.xlabel('Stage')
    plt.ylabel('Users')
    plt.xticks(rotation=20, ha='right')
    plt.tight_layout()
    plt.savefig(img_dir / 'funnel_overall.png', dpi=160)
    plt.close()

    dep = funnel_by_source[funnel_by_source['stage'] == 'Deposit made'].copy()
    landing = funnel_by_source[funnel_by_source['stage'] == 'Landing viewed'][['source', 'users']].rename(columns={'users': 'landing_users'})
    dep = dep.merge(landing, on='source', how='left')
    dep['deposit_rate'] = dep['users'] / dep['landing_users']
    dep = dep.sort_values('deposit_rate', ascending=False)

    plt.figure(figsize=(9, 5))
    plt.bar(dep['source'], dep['deposit_rate'])
    plt.title('Landing → Deposit conversion by source')
    plt.xlabel('Source')
    plt.ylabel('Conversion')
    plt.tight_layout()
    plt.savefig(img_dir / 'deposit_rate_by_source.png', dpi=160)
    plt.close()

    print("Analysis completed successfully.")

if __name__ == "__main__":
    main()
