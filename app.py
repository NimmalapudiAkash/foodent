import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

const FoodAnalyzerDemo = () => {
  const [selectedExample, setSelectedExample] = useState('tomato');

  const examples = {
    tomato: {
      name: "Tomato Pasta",
      colors: {
        red: "45.2%",
        brown: "25.5%",
        light: "20.3%",
        green: "9.0%"
      },
      analysis: {
        type: "Red dominant dish",
        calories: 250,
        healthScore: 75,
        nutrients: {
          protein: "8g",
          carbs: "30g",
          fat: "12g",
          fiber: "4g"
        }
      }
    },
    salad: {
      name: "Green Salad",
      colors: {
        green: "52.1%",
        light: "28.4%",
        red: "12.3%",
        brown: "7.2%"
      },
      analysis: {
        type: "Green dominant dish",
        calories: 150,
        healthScore: 95,
        nutrients: {
          protein: "5g",
          carbs: "15g",
          fat: "7g",
          fiber: "8g"
        }
      }
    },
    sandwich: {
      name: "Sandwich",
      colors: {
        brown: "48.6%",
        light: "32.1%",
        green: "10.2%",
        red: "9.1%"
      },
      analysis: {
        type: "Brown dominant dish",
        calories: 350,
        healthScore: 65,
        nutrients: {
          protein: "12g",
          carbs: "45g",
          fat: "15g",
          fiber: "3g"
        }
      }
    }
  };

  const selected = examples[selectedExample];

  return (
    <Card className="w-full max-w-3xl">
      <CardHeader>
        <CardTitle>Food Analyzer Demo</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <div className="flex space-x-4">
            {Object.keys(examples).map((key) => (
              <button
                key={key}
                onClick={() => setSelectedExample(key)}
                className={`px-4 py-2 rounded ${
                  selectedExample === key
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-100'
                }`}
              >
                {examples[key].name}
              </button>
            ))}
          </div>

          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-4">
              <h3 className="font-semibold">Color Analysis</h3>
              <div className="space-y-2">
                {Object.entries(selected.colors).map(([color, percentage]) => (
                  <div key={color} className="flex items-center space-x-2">
                    <div 
                      className="w-4 h-4 rounded"
                      style={{
                        backgroundColor: color === 'light' ? '#f0f0f0' : color
                      }}
                    />
                    <span className="capitalize">{color}:</span>
                    <span className="font-semibold">{percentage}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="font-semibold">Analysis Results</h3>
              <div className="space-y-2">
                <p>Type: {selected.analysis.type}</p>
                <p>Calories: {selected.analysis.calories}</p>
                <p>Health Score: {selected.analysis.healthScore}/100</p>
                <div className="mt-4">
                  <p className="font-semibold">Nutrients:</p>
                  <div className="grid grid-cols-2 gap-2">
                    {Object.entries(selected.analysis.nutrients).map(([nutrient, value]) => (
                      <p key={nutrient} className="capitalize">
                        {nutrient}: {value}
                      </p>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default FoodAnalyzerDemo;
