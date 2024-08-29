import express from 'express';
import Redis from 'ioredis';

const redis = new Redis();

const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 }
];

const getItemById = (id) => listProducts.find(item => item.id === id);

const app = express();
const port = 1245;

app.get('/list_products', (req, res) => {
  const products = listProducts.map(({ id, name, price, stock }) => ({
    itemId: id,
    itemName: name,
    price,
    initialAvailableQuantity: stock
  }));
  res.json(products);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const item = getItemById(itemId);

  if (!item) {
    return res.json({ status: 'Product not found' });
  }

  const currentQuantity = await getCurrentReservedStockById(itemId);

  res.json({
    itemId: item.id,
    itemName: item.name,
    price: item.price,
    initialAvailableQuantity: item.stock,
    currentQuantity
  });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const item = getItemById(itemId);

  if (!item) {
    return res.json({ status: 'Product not found' });
  }

  const currentQuantity = await getCurrentReservedStockById(itemId);

  if (currentQuantity >= item.stock) {
    return res.json({
      status: 'Not enough stock available',
      itemId: item.id
    });
  }

  await reserveStockById(itemId, currentQuantity + 1);
  res.json({
    status: 'Reservation confirmed',
    itemId: item.id
  });
});

const reserveStockById = (itemId, stock) => {
  return redis.set(`item.${itemId}`, stock);
};

const getCurrentReservedStockById = async (itemId) => {
  const stock = await redis.get(`item.${itemId}`);
  return stock ? parseInt(stock, 10) : 0;
};

app.listen(port, () => {
  console.log(`Server is running on http:
});
