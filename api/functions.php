<?php
declare(strict_types=1);

require_once __DIR__ . '/config.php';

function fetch_json(string $url): array
{
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array(
            $ch,
            [
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_TIMEOUT => 8,
                CURLOPT_CONNECTTIMEOUT => 5,
                CURLOPT_SSL_VERIFYPEER => true,
            ]
        );
        $response = curl_exec($ch);
        $error = curl_error($ch);
        $status = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($response === false) {
            return ['ok' => false, 'error' => $error ?: 'Request failed.'];
        }
        if ($status < 200 || $status >= 300) {
            return ['ok' => false, 'error' => "HTTP error {$status}."];
        }
        $json = json_decode($response, true);
        if (!is_array($json)) {
            return ['ok' => false, 'error' => 'Invalid JSON response.'];
        }
        return ['ok' => true, 'data' => $json];
    }

    $context = stream_context_create(
        [
            'http' => [
                'method' => 'GET',
                'timeout' => 8,
            ],
        ]
    );
    $response = @file_get_contents($url, false, $context);
    if ($response === false) {
        return ['ok' => false, 'error' => 'Unable to fetch response.'];
    }
    $json = json_decode($response, true);
    if (!is_array($json)) {
        return ['ok' => false, 'error' => 'Invalid JSON response.'];
    }
    return ['ok' => true, 'data' => $json];
}

function getWeather(string $city = 'Mumbai'): array
{
    $apiKey = app_env('OPENWEATHER_API_KEY', '');
    if (!$apiKey) {
        return ['ok' => false, 'error' => 'Weather API key not configured.'];
    }
    $city = trim($city) !== '' ? trim($city) : 'Mumbai';
    $url = 'https://api.openweathermap.org/data/2.5/weather?q='
        . rawurlencode($city)
        . '&appid=' . rawurlencode($apiKey)
        . '&units=metric';

    $result = fetch_json($url);
    if (!$result['ok']) {
        return ['ok' => false, 'error' => $result['error']];
    }
    $payload = $result['data'];
    if (($payload['cod'] ?? 200) !== 200) {
        return ['ok' => false, 'error' => $payload['message'] ?? 'Weather fetch failed.'];
    }
    return ['ok' => true, 'data' => $payload];
}

function getNews(string $country = 'in', int $limit = 6): array
{
    $apiKey = app_env('NEWS_API_KEY', '');
    if (!$apiKey) {
        return ['ok' => false, 'error' => 'News API key not configured.'];
    }

    $url = 'https://newsapi.org/v2/top-headlines?country='
        . rawurlencode($country)
        . '&pageSize=' . max(1, min($limit, 10))
        . '&apiKey=' . rawurlencode($apiKey);

    $result = fetch_json($url);
    if (!$result['ok']) {
        return ['ok' => false, 'error' => $result['error']];
    }
    $payload = $result['data'];
    if (($payload['status'] ?? 'error') !== 'ok') {
        return ['ok' => false, 'error' => $payload['message'] ?? 'News fetch failed.'];
    }
    return ['ok' => true, 'data' => $payload];
}
