for url in "$@"; do
  sha=$(curl -sSL "$url" | openssl dgst -sha384 -binary | openssl base64 -A)
  echo "$url: sha384-$sha"
done
