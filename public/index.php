<?php
declare(strict_types=1);

require_once __DIR__ . '/../api/functions.php';

function h(string $value): string
{
    return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}

$city = trim((string) ($_GET['city'] ?? 'Mumbai'));
$weather = getWeather($city);
$news = getNews('in', 8);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JarvisAI - Smart Voice Assistant</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <main class="shell">
        <header class="hero">
            <p class="kicker">Voice Assistant Dashboard</p>
            <h1>JarvisAI</h1>
            <p class="subtitle">Real-time weather and top headlines with browser voice control.</p>
        </header>

        <section class="voice-card">
            <button id="micBtn" type="button" class="btn-primary">Talk to Jarvis</button>
            <p id="voiceStatus" class="status">Status: Idle</p>
            <p id="voiceOutput" class="output">Voice output will appear here.</p>
        </section>

        <section class="grid">
            <article class="panel" id="weatherPanel">
                <h2>Weather Update</h2>
                <?php if ($weather['ok']): ?>
                    <?php $w = $weather['data']; ?>
                    <p class="meta"><?= h((string) ($w['name'] ?? $city)); ?></p>
                    <p class="temp"><?= h((string) round((float) ($w['main']['temp'] ?? 0), 1)); ?>&deg;C</p>
                    <p><?= h((string) ($w['weather'][0]['description'] ?? 'N/A')); ?></p>
                    <p>Humidity: <?= h((string) ($w['main']['humidity'] ?? 'N/A')); ?>%</p>
                    <p>Wind: <?= h((string) ($w['wind']['speed'] ?? 'N/A')); ?> m/s</p>
                <?php else: ?>
                    <p class="error">Weather unavailable: <?= h($weather['error']); ?></p>
                <?php endif; ?>
            </article>

            <article class="panel" id="newsPanel">
                <h2>Top News</h2>
                <?php if ($news['ok'] && !empty($news['data']['articles'])): ?>
                    <ul class="news-list">
                        <?php foreach ($news['data']['articles'] as $article): ?>
                            <li>
                                <a href="<?= h((string) ($article['url'] ?? '#')); ?>" target="_blank" rel="noopener noreferrer">
                                    <?= h((string) ($article['title'] ?? 'Untitled')); ?>
                                </a>
                            </li>
                        <?php endforeach; ?>
                    </ul>
                <?php else: ?>
                    <p class="error">News unavailable: <?= h((string) ($news['error'] ?? 'No articles found.')); ?></p>
                <?php endif; ?>
            </article>
        </section>
    </main>

    <script src="js/main.js"></script>
</body>
</html>
