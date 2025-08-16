import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";

interface SettingsProps {
  customerId?: number | null;
}

export default function Settings({ customerId }: SettingsProps) {
  return (
    <div className="p-6 space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
      </div>

      {/* Settings Tabs */}
      <Tabs defaultValue="account" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="account">Account</TabsTrigger>
          <TabsTrigger value="preferences">Preferences</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="api">API & Integrations</TabsTrigger>
        </TabsList>

        {/* Account Tab */}
        <TabsContent value="account" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Profile Information</CardTitle>
              <p className="text-sm text-gray-600">Update your account details</p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="firstName">First Name</Label>
                  <Input
                    id="firstName"
                    placeholder="Alex"
                    defaultValue="Alex"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="lastName">Last Name</Label>
                  <Input
                    id="lastName"
                    placeholder="Johnson"
                    defaultValue="Johnson"
                  />
                </div>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="alex.johnson@example.com"
                  defaultValue="alex.johnson@example.com"
                />
              </div>

              <Button className="bg-blue-600 hover:bg-blue-700">
                Save Changes
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Password</CardTitle>
              <p className="text-sm text-gray-600">Update your password</p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="currentPassword">Current Password</Label>
                <Input
                  id="currentPassword"
                  type="password"
                  placeholder="Enter current password"
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="newPassword">New Password</Label>
                  <Input
                    id="newPassword"
                    type="password"
                    placeholder="Enter new password"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="confirmPassword">Confirm Password</Label>
                  <Input
                    id="confirmPassword"
                    type="password"
                    placeholder="Confirm new password"
                  />
                </div>
              </div>

              <Button variant="outline">
                Update Password
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Preferences Tab */}
        <TabsContent value="preferences" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Display Preferences</CardTitle>
              <p className="text-sm text-gray-600">Customize your dashboard experience</p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-base font-medium">Dark Mode</Label>
                  <p className="text-sm text-gray-600">Enable dark theme for the interface</p>
                </div>
                <Switch />
              </div>

              <div className="space-y-2">
                <Label>Default Currency</Label>
                <select className="w-full px-3 py-2 border border-gray-200 rounded-lg" defaultValue="USD">
                  <option value="USD">USD - US Dollar</option>
                  <option value="EUR">EUR - Euro</option>
                  <option value="GBP">GBP - British Pound</option>
                  <option value="JPY">JPY - Japanese Yen</option>
                </select>
              </div>

              <div className="space-y-2">
                <Label>Default Market</Label>
                <select className="w-full px-3 py-2 border border-gray-200 rounded-lg" defaultValue="US">
                  <option value="US">United States</option>
                  <option value="EU">European Union</option>
                  <option value="ASIA">Asia Pacific</option>
                  <option value="GLOBAL">Global</option>
                </select>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-base font-medium">Show Advanced Charts</Label>
                  <p className="text-sm text-gray-600">Display technical analysis charts</p>
                </div>
                <Switch defaultChecked />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Investment Preferences</CardTitle>
              <p className="text-sm text-gray-600">Set your investment goals and risk tolerance</p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label>Risk Tolerance</Label>
                <select className="w-full px-3 py-2 border border-gray-200 rounded-lg" defaultValue="moderate">
                  <option value="conservative">Conservative</option>
                  <option value="moderate">Moderate</option>
                  <option value="aggressive">Aggressive</option>
                </select>
              </div>

              <div className="space-y-2">
                <Label>Investment Horizon</Label>
                <select className="w-full px-3 py-2 border border-gray-200 rounded-lg" defaultValue="long">
                  <option value="short">Short Term (&lt; 2 years)</option>
                  <option value="medium">Medium Term (2-5 years)</option>
                  <option value="long">Long Term (&gt; 5 years)</option>
                </select>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-base font-medium">ESG Investing</Label>
                  <p className="text-sm text-gray-600">Focus on environmental, social, and governance factors</p>
                </div>
                <Switch />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Notifications Tab */}
        <TabsContent value="notifications" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Notification Preferences</CardTitle>
              <p className="text-sm text-gray-600">Manage how you receive notifications</p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-base font-medium">Email Notifications</Label>
                  <p className="text-sm text-gray-600">Receive portfolio updates via email</p>
                </div>
                <Switch defaultChecked />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-base font-medium">Push Notifications</Label>
                  <p className="text-sm text-gray-600">Get instant notifications on your device</p>
                </div>
                <Switch defaultChecked />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-base font-medium">Market Alerts</Label>
                  <p className="text-sm text-gray-600">Alerts for significant market movements</p>
                </div>
                <Switch defaultChecked />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-base font-medium">Price Alerts</Label>
                  <p className="text-sm text-gray-600">Notifications when stocks hit target prices</p>
                </div>
                <Switch defaultChecked />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-base font-medium">News Alerts</Label>
                  <p className="text-sm text-gray-600">Breaking financial news notifications</p>
                </div>
                <Switch />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-base font-medium">AI Recommendations</Label>
                  <p className="text-sm text-gray-600">New AI-generated investment recommendations</p>
                </div>
                <Switch defaultChecked />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* API & Integrations Tab */}
        <TabsContent value="api" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>API Configuration</CardTitle>
              <p className="text-sm text-gray-600">Manage external API connections</p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="apiKey">API Key</Label>
                <div className="flex gap-2">
                  <Input
                    id="apiKey"
                    type="password"
                    value="••••••••••••••••••••••••••••••••"
                    readOnly
                  />
                  <Button variant="outline">
                    Regenerate
                  </Button>
                </div>
                <p className="text-xs text-gray-500">
                  Keep your API key secure and don't share it with others
                </p>
              </div>

              <div className="space-y-4">
                <Label className="text-base font-medium">Connected Services</Label>
                
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                    <div>
                      <h4 className="font-medium">OpenAI Integration</h4>
                      <p className="text-sm text-gray-600">AI-powered analysis and recommendations</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-sm text-green-600">Connected</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                    <div>
                      <h4 className="font-medium">Market Data Provider</h4>
                      <p className="text-sm text-gray-600">Real-time market data and pricing</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-sm text-green-600">Connected</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                    <div>
                      <h4 className="font-medium">News Intelligence</h4>
                      <p className="text-sm text-gray-600">Financial news and sentiment analysis</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                      <span className="text-sm text-yellow-600">Limited</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Data Export</CardTitle>
              <p className="text-sm text-gray-600">Export your portfolio data</p>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium">Portfolio Data</h4>
                  <p className="text-sm text-gray-600">Export your current holdings and performance</p>
                </div>
                <Button variant="outline">
                  Export CSV
                </Button>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium">Transaction History</h4>
                  <p className="text-sm text-gray-600">Download complete transaction records</p>
                </div>
                <Button variant="outline">
                  Export PDF
                </Button>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium">AI Recommendations</h4>
                  <p className="text-sm text-gray-600">Export AI-generated recommendations</p>
                </div>
                <Button variant="outline">
                  Export JSON
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
