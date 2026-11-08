import { generateKeyPairSync } from 'node:crypto';
import { mkdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

// Deliberately outside source control; never print private keys or replace an existing pair.
const directory = fileURLToPath(new URL('../backend/data/', import.meta.url));
const target = fileURLToPath(new URL('../backend/data/push.local.env', import.meta.url));
const { publicKey, privateKey } = generateKeyPairSync('ec', { namedCurve: 'prime256v1' });
const pub = publicKey.export({ format: 'jwk' });
const priv = privateKey.export({ format: 'jwk' });
const encoded = Buffer.concat([Buffer.from([4]), Buffer.from(pub.x, 'base64url'), Buffer.from(pub.y, 'base64url')]).toString('base64url');
mkdirSync(directory, { recursive: true });
try {
  writeFileSync(target, [
    'CLASSFORGE_PUSH_ENABLED=false',
    `CLASSFORGE_PUSH_PUBLIC_KEY=${encoded}`,
    `CLASSFORGE_PUSH_PRIVATE_KEY=${priv.d}`,
    'CLASSFORGE_PUSH_SUBJECT=mailto:CHANGE_ME@example.invalid',
    '',
  ].join('\n'), { flag: 'wx', mode: 0o600 });
  console.log(`Claves guardadas en ${target}. Configura subject y activa push cuando vayas a probarlo.`);
} catch (error) {
  if (error.code === 'EEXIST') {
    console.error('Ya existe push.local.env. Se conservó la pareja de claves existente.');
    process.exitCode = 1;
  } else throw error;
}
