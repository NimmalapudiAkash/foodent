import React, { useState } from 'react';
import { Camera, Upload, Lock } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert';

const FoodAnalysisApp = () => {
  const [foodData, setFoodData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Function to handle file upload
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    
    try {
      setIsLoading(true);
      setError('');
      
      // In a real app, you would:
      // 1. Get the API key from environment variables
      // 2. Send the image to your backend
      // 3. Process the image and return food data
      // For demo, we'll simulate an API response
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setFoodData({
        name: "Sample Food",
        calories: 250,
        nutrients: {
          protein: "10g",
          carbs: "30g",
          fat: "12g"
        }
      });
    } catch (err) {
      setError('Error analyzing food image. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle camera capture
  const handleCameraCapture = () => {
    // In a real app, you would implement camera functionality
    alert('Camera functionality would be implemented here');
  };

  return (
    <div className="max-w-2xl mx-auto p-4 space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Lock className="w-5 h-5" />
            Food Analysis App
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex gap-4 justify-center">
              <label className="flex flex-col items-center gap-2 cursor-pointer p-4 border-2 border-dashed rounded-lg hover:bg-gray-50">
                <Upload className="w-8 h-8 text-blue-500" />
                <span className="text-sm">Upload Photo</span>
                <input
                  type="file"
                  className="hidden"
                  accept="image/*"
                  onChange={handleFileUpload}
                />
              </label>
              
              <button
                onClick={handleCameraCapture}
                className="flex flex-col items-center gap-2 p-4 border-2 border-dashed rounded-lg hover:bg-gray-50"
              >
                <Camera className="w-8 h-8 text-blue-500" />
                <span className="text-sm">Take Photo</span>
              </button>
            </div>

            {isLoading && (
              <div className="text-center py-4">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
                <p className="mt-2 text-sm text-gray-600">Analyzing food...</p>
              </div>
            )}

            {error && (
              <Alert variant="destructive">
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {foodData && (
              <Card>
                <CardHeader>
                  <CardTitle>Analysis Results</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <p className="text-lg font-semibold">{foodData.name}</p>
                    <p className="text-gray-600">Calories: {foodData.calories}</p>
                    <div className="grid grid-cols-3 gap-4">
                      <div className="p-2 bg-blue-50 rounded">
                        <p className="font-medium">Protein</p>
                        <p>{foodData.nutrients.protein}</p>
                      </div>
                      <div className="p-2 bg-green-50 rounded">
                        <p className="font-medium">Carbs</p>
                        <p>{foodData.nutrients.carbs}</p>
                      </div>
                      <div className="p-2 bg-yellow-50 rounded">
                        <p className="font-medium">Fat</p>
                        <p>{foodData.nutrients.fat}</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default FoodAnalysisApp;
