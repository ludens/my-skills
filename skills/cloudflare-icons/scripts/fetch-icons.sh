#!/usr/bin/env bash
# Download Cloudflare icon SVGs from cf-icons.pages.dev.
#
# Usage:
#   bash fetch-icons.sh OUTPUT_DIR SLUG [SLUG...]
#   bash fetch-icons.sh OUTPUT_DIR --all          # 78 service icons
#   bash fetch-icons.sh OUTPUT_DIR --extras       # 29 architecture / Zero Trust / logo icons
#   bash fetch-icons.sh OUTPUT_DIR --components   # curated component icons
#   bash fetch-icons.sh OUTPUT_DIR --everything   # all of the above
#
# CF_ICONS_BASE overrides the base URL (default: https://cf-icons.pages.dev).

set -euo pipefail

BASE="${CF_ICONS_BASE:-https://cf-icons.pages.dev}"

SERVICE_SLUGS=(
  1.1.1.1 ai-gateway ai analytics api-shield api apps argo-smart-routing
  automatic-platform-optimization bots browser-rendering byoip cache calls
  china-network client-ip-geolocation cloudflare-for-platforms cloudflare-one
  constellation d1 data-localization ddos-protection dmarc-management dns
  docs-guide durable-objects email-routing email-security firewall fundamentals
  health-checks hyperdrive images kv learning-paths load-balancing logs
  magic-firewall magic-network-monitoring magic-transit magic-wan
  network-error-logging network-interconnect notifications page-shield pages
  privacy-gateway pub-sub pulumi queues r2 radar railgun randomness-beacon
  reference-architecture registrar rules ruleset-engine security-center spectrum
  speed ssl stream style-guide support tenant terraform time-services turnstile
  vectorize version-management waf waiting-room warp-client web3 workers-ai
  workers zaraz
)

EXTRA_SLUGS=(
  AndroidLaptop AndroidPhone AndroidTablet AppleLaptop ApplePhone AppleTablet
  ChromeLaptop ChromePhone ChromeTablet Cloudflared Google Onetimepin
  WarpConnector WindowsLaptop WindowsPhone WindowsTablet ZeroTrustLogo azureAD
  cloud-internet cloud-multi internet-globe office-headquarters router
  security-fingerprint-privacy server-database logo logo-inline logo-cloud
  pages-logo
)

# Component icons that are useful in architecture diagrams but are not in the
# 78 service icon list displayed on cf-icons.pages.dev.
COMPONENT_SLUGS=(
  cloudflare-access cloudflare-zero-trust cloudflare-dex
  cloudflare-security-application cloudflare-security-network api-security
  gateway teams dlp zerotrust-casb-logo zerotrust-networks-logo
  zero-trust-risk-scoring network-security security-bots security-waf
  product-security-center firewall-rules reliability-dns
  reliability-load-balancer network server-origin office-branch
  workers-bundled workers-for-platforms workers-kv workers-pages workers-unbound
  workers-durable-objects workers-constellation wrangler tail-worker
  magic-transit-logo registrar-logo web-analytics-logo account-analytics-logo
  optimization-scale traffic-attack-browser ddos-attack email-forwarding
  device-desktop device-laptop device-mobile internet-browser globe flowchart
)

usage() {
  sed -n '3,11p' "$0" | sed 's/^# \{0,1\}//'
  exit 2
}

[ "$#" -ge 2 ] || usage

OUT_DIR="$1"
shift

selected=()
case "$1" in
  --all) selected=("${SERVICE_SLUGS[@]}") ;;
  --extras) selected=("${EXTRA_SLUGS[@]}") ;;
  --components) selected=("${COMPONENT_SLUGS[@]}") ;;
  --everything) selected=("${SERVICE_SLUGS[@]}" "${EXTRA_SLUGS[@]}" "${COMPONENT_SLUGS[@]}") ;;
  *) selected=("$@") ;;
esac

mkdir -p "$OUT_DIR"

ok=0
failed=()
for slug in "${selected[@]}"; do
  target="$OUT_DIR/$slug.svg"
  tmp="$target.tmp"

  if ! curl -fsSL --retry 3 --retry-delay 1 "$BASE/$slug.svg" -o "$tmp"; then
    rm -f "$tmp"
    failed+=("$slug (download failed)")
    continue
  fi

  if ! grep -q '<svg' "$tmp" || ! grep -q 'viewBox=' "$tmp"; then
    rm -f "$tmp"
    failed+=("$slug (not an SVG; check the slug)")
    continue
  fi

  mv "$tmp" "$target"
  ok=$((ok + 1))
done

echo "Downloaded $ok/${#selected[@]} icons to $OUT_DIR"

if [ "${#failed[@]}" -gt 0 ]; then
  echo "Failed:" >&2
  printf '  - %s\n' "${failed[@]}" >&2
  exit 1
fi
